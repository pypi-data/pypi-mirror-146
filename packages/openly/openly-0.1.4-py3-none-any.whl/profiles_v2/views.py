import sys
import json

from collections import defaultdict
from functools import reduce
from dashboard import charts
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    BeautifulSoup = None
from django.conf import settings
from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.safestring import mark_safe
from urllib.parse import unquote
from django.views.generic import TemplateView, View
from django.views.generic.edit import UpdateView, CreateView
from rest_framework import generics, permissions, viewsets

from aims import aggregates as agg
from aims import models as aims
from aims import base_utils
from aims.api_serializers import serializers
from aims.utils import render

from .forms import ContactForm, PersonForm, ImageUploadForm
from .models import OrganisationContactInfo, OrganisationProfile, Person, Contact
from .permissions import OrganisationContactInfoPermission, OrganisationProfilePermission, PersonPermission
from .serializers import OrganisationContactInfoSerializer, OrganisationProfileSerializer, PersonSerializer


DATE_FORMAT = '%d %b %Y'


class OrganisationActivities(View):
    '''
    View to return a JSON representation of the activities
    which the organisation is involved in via
    APO or as reporter
    '''

    def get(self, *args, **kwargs):
        '''
        A GET request should return a serialized list
        of related activities
        '''
        acts, keys = aims.Organisation.objects.get(pk=kwargs.get('organisation')).activities
        values = (
            'pk',
            'internal_identifier',
            'iati_identifier',
            'activity_status',
            'activity_status__name',
            'reporting_organisation__name',
            'reporting_organisation__pk',
            'activity_status',
            'start_actual',
            'end_actual',
            'start_planned',
            'end_planned',
            'completion',
            'last_updated_datetime',
            'date_created',
            'date_modified',
            *keys
        )
        activities = list(acts.values(*values))

        implementing_partners = defaultdict(list)
        for activity, organisation, organisation_name in aims.ActivityParticipatingOrganisation.objects.filter(role='Implementing', activity__in=acts).values_list('activity', 'organisation', 'organisation__name'):
            implementing_partners[activity].append(organisation_name or organisation)

        return JsonResponse(
            data={
                'activities': activities,
                'implementing_partners': implementing_partners,
                'activity_count': len(activities),  # acts.count(),
                'choices': {
                    'status': list(aims.ActivityStatus.objects.all().values('pk', 'name')),
                    'reporting_organisation': list(acts.order_by().distinct('reporting_organisation').values('reporting_organisation__pk', 'reporting_organisation__name')),
                    'role': list(acts.order_by().distinct('role').values('role'))
                }
            },
            json_dumps_params={'indent': 1}
        )


class OrganisationProfileView(TemplateView):
    """ View for an organisation's profile.
    The organisation must exist but if the profile doesn't already exist then create one.
    """
    template_name = "profiles_v2/organisation_profile.html"

    def get_context_data(self, **kwargs):
        context = super(OrganisationProfileView,
                        self).get_context_data(**kwargs)

        donor_code = self.kwargs['iati_identifier'] if 'iati_identifier' in kwargs else '0'

        # Path must correspond to an existing organisation
        organisation = get_object_or_404(
            aims.Organisation.objects, code=unquote(donor_code))

        # If the profile doesn't exist then create it and provide some special handling for
        # the background field which is translatable
        organisation_profile, _ = OrganisationProfile.objects.get_or_create(
            organisation=organisation
        )
        # Set the  translation fields from the optional ModelTranslation languages setting,
        # falling back to LANGUAGES if that is not defined
        background_translations = {
            code: getattr(organisation_profile, 'background_{}'.format(code))
            for code in getattr(
                settings, 'MODELTRANSLATION_LANGUAGES',
                [lang[0] for lang in getattr(settings, 'LANGUAGES')]
            )
        }

        # If the organisation's contact info doesn't exist then create it
        contact_info, _ = OrganisationContactInfo.objects.get_or_create(
            profile=organisation_profile
        )

        # Can the user edit?
        editor = base_utils.check_editor_privilege(
            self.request.user, organisation)

        sectors = None

        if getattr(settings, 'FINANCIAL_DATA_EXISTS', False):
            sectors = list(agg.organisation_commitment_by_sector(organisation.code))
            context['aid_type_category_breakdown'] = defaultdict(int)
            context['aid_type_breakdown'] = defaultdict(int)
            transaction_queryset = aims.Transaction.objects.filter(
                provider_organisation=organisation)
            for each_transaction in transaction_queryset.filter(transaction_type_id='C').values('usd_value', 'aid_type__name', 'aid_type__category__name'):
                context['aid_type_breakdown'][each_transaction['aid_type__name']
                                              ] += each_transaction['usd_value'] or 0
                context['aid_type_category_breakdown'][each_transaction['aid_type__category__name']
                                                       ] += each_transaction['usd_value'] or 0
            context['aid_type_category_breakdown'] = [(k if k else "No Aid Type Category", round(
                v), base_utils.prettify_compact(v)) for k, v in context['aid_type_category_breakdown'].items()]
            context['aid_type_breakdown'] = [(k if k else "No Aid Type", round(
                v), base_utils.prettify_compact(v)) for k, v in context['aid_type_breakdown'].items()]

        # Embed the above in the context along with some static data languages/areas and
        # serialized representations of the activities and people assocaited with the
        # organisation
        context['donor'] = donor_code
        context['page_title'] = organisation.name
        context['organisation_profile'] = organisation_profile
        context['organisation_code'] = organisation.pk
        context['organisation'] = organisation
        context['background_translations'] = background_translations
        context['contact_info'] = render(
            OrganisationContactInfoSerializer(contact_info).data
        )

        # check if financial data does not exist OR commitment lookup returned empty list
        if not sectors or sectors == []:
            sectors = aims.SectorCategory.objects.filter(
                sector__activitysector__vocabulary='DAC-5',
                sector__activitysector__activity__participating_organisations__organisation=organisation,
                sector__activitysector__activity__openly_status='published',
            ).values('code', 'name').distinct()
        context['sectors'] = render(sectors)

        try:
            context['map_config'] = render(settings.LEAFLET_CONFIG)
        except Exception:
            context['map_config'] = render({})
        context['person_model'] = Person
        people = PersonSerializer(organisation_profile.people.order_by('order'), many=True).data
        # remove sensitive contact data if user is not authorized
        if not self.request.user.is_authenticated:
            for p in people:
                p['phone_number'] = ''
                p['email'] = ''
        context['people'] = people
        context['activities'] = []  # Deprecated
        context['activity_count'] = organisation.count_activities
        context['languages'] = render(
            [{'language_code': k, 'language_name': v} for (k, v) in settings.LANGUAGES])
        context['token'] = self.request.META.get('CSRF_COOKIE', None)
        context['editor'] = editor
        context['financial_data_exists'] = getattr(settings, 'FINANCIAL_DATA_EXISTS', False)
        context['project_name'] = getattr(settings, 'PROJECT_NAME', "")
        # Resources for Organisation Profiles
        context['resources_in_profile'] = getattr(settings, 'RESOURCES_IN_PROFILE', False)
        if context['resources_in_profile']:
            resources = aims.DocumentLink.objects.filter(organisation=organisation).filter(language=self.request.LANGUAGE_CODE)
            if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.organisation and self.request.user.organisation == organisation):
                # auth users with an Org matching profile's see ALL resources
                resources = resources.all().order_by('-date_modified')
            else:
                # public users OR auth users (w/o same org) see only PUBLIC resources
                resources = resources.exclude(private=True).all().order_by('-date_modified')
            resources_list = []
            for doc in resources[:5]:
                doc_cats = doc.categories.all()
                if doc.activity:
                    activity = doc.activity.title
                else:
                    activity = None
                if len(doc.narrative.all()) > 0:
                    description = doc.narrative.all()[0].description
                else:
                    description = None
                if hasattr(doc, 'upload'):
                    try:
                        size = doc.upload.doc.size
                        file_type = doc.file_format.code
                    except FileNotFoundError:
                        size = None
                        file_type = None
                else:
                    size = None
                    file_type = None
                resources_list.append({
                    'title': doc.title,
                    'description': description,
                    'activity': activity,
                    'url': doc.url,
                    'iso_date': doc.iso_date.strftime("%Y/%m/%d"),
                    'size': size,
                    'file_type': file_type,
                    'categories': [c.name for c in doc_cats] if len(doc_cats) > 0 else None
                })
            context['resources'] = mark_safe(json.dumps(resources_list))
            context['resource_count'] = len(resources)
        else:
            context['resource_count'] = 0

        # This is legacy code from the days when Maps and Finances were never in the same
        # project and should be revised
        if not context['financial_data_exists']:
            context['areas'] = render(
                {area.pk: serializers.AreaSerializer(area).data for area in aims.Area.objects.all()})
        else:
            context['areas'] = {}
        context['donor_locations_allowed'] = getattr(settings, 'DONOR_LOCATIONS_ALLOWED', True)
        context['riot3'] = True
        return context


class UpdateGenericView(View):
    """ Generic view allowing posting updates to a django model with basic functionality for
    casting the inputted 'string' data into a different type and sanitizing any html.
    """

    def boolify(self, s):
        if s == 'True' or s == 'true':
            return True
        if s == 'False' or s == 'false':
            return False
        if s == 'None' or s == 'none':
            return None
        raise ValueError('Not Boolean Value!')

    def automatic_cast(self, var):
        var = str(var)
        for caster in (self.boolify, int, float):
            try:
                return caster(var)
            except ValueError:
                pass
        return var

    def sanitize_html(self, html):
        if not BeautifulSoup:
            return html
        VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br']
        soup = BeautifulSoup(html, 'html')

        for tag in soup.findAll(True):
            if tag.name not in VALID_TAGS:
                tag.hidden = True

        return str(soup.renderContents()).replace('"', '&quot;')[2:-1]

    def post(self, *args, **kwargs):

        class_name = self.request.POST['class']
        pk = self.request.POST['pk']
        field_name = self.request.POST['name']

        # Get the data as string or array
        try:
            field_value = self.request.POST['value']
            if not field_value:
                field_value = None
        except MultiValueDictKeyError:
            field_value = self.request.POST.getlist('value[]')

        # Cast the data to a different type if necessary
        if 'cast' in self.request.POST.keys():
            field_value = self.automatic_cast(field_value)
        # Sanitize any html
        if 'is_html' in self.request.POST.keys():
            field_value = self.sanitize_html(field_value)

        # Find the class object type and get the specified object
        cls = reduce(getattr, class_name.split('.')[
            1:], sys.modules[class_name.split('.')[0]])
        instance = cls.objects.get(pk=pk)

        # Save the data
        if type(field_value) == list:
            attr = getattr(instance, field_name)
            attr.clear()
            for i in field_value:
                attr.add(i)
        else:
            setattr(instance, field_name, field_value)
            instance.save()

        return HttpResponse()


class UploadGenericView(View):
    """ Generic view allowing users to upload
    images to be saved in a model's ImageField
    """

    def post(self, *args, **kwargs):

        class_name = self.request.POST['class']
        pk = self.request.POST['pk']
        field_name = self.request.POST['name']

        # Validate that image has an allowed format
        form = ImageUploadForm(self.request.POST, self.request.FILES)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)

        # Find the specified model in the database
        cls = reduce(getattr, class_name.split('.')[
            1:], sys.modules[class_name.split('.')[0]])
        instance = cls.objects.get(pk=pk)

        # Update its image field
        setattr(instance, field_name, form.cleaned_data['image'])
        instance.save()
        instance.resize_image(field_name)

        data = {'image': getattr(instance, field_name).url}
        return JsonResponse(data)


# Some basic DRF views/viewsets used as the API endpoints
class RetrieveUpdateOrganisationProfileView(generics.RetrieveUpdateAPIView):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer
    permission_classes = (permissions.IsAuthenticated,
                          OrganisationProfilePermission)
    lookup_field = 'organisation__pk'


class RetrieveUpdateOrganisationContactInfoView(generics.RetrieveUpdateAPIView):
    queryset = OrganisationContactInfo.objects.all()
    serializer_class = OrganisationContactInfoSerializer
    permission_classes = (permissions.IsAuthenticated,
                          OrganisationContactInfoPermission)
    lookup_field = 'profile__organisation__pk'


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated, PersonPermission)

    def get_queryset(self):
        # Generally we only want to get the people attached to a specific organisation
        if 'organisation_pk' in self.request.GET:
            try:
                return Person.objects.filter(organisation_profile__organisation__pk=self.request.GET['organisation_pk']).order_by('order')
            except SyntaxError:
                return []
        return Person.objects.all()


# PROFILES V1 views pulled over
class DonorCommitmentByCategory(View):
    ''' returns commitment by category json for a given donor'''

    def get(self, *args, **kwargs):
        donor_code = self.kwargs['iati_identifier'] if 'iati_identifier' in kwargs else '0'

        organisation = get_object_or_404(
            aims.Organisation.objects, code=unquote(donor_code))
        transaction_queryset = aims.Transaction.objects.filter(
            provider_organisation=organisation
        )
        commitment_by_category = charts.commitment_by_category(
            aims.Activity.objects.all(), transaction_queryset, 20, False)
        return JsonResponse(commitment_by_category, safe=False)


class DonorActivityStatusValues(View):
    ''' returns activity details by status for a given donor'''

    def get(self, *args, **kwargs):
        donor_code = self.kwargs['iati_identifier'] if 'iati_identifier' in kwargs else '0'

        organisation = get_object_or_404(
            aims.Organisation.objects, code=unquote(donor_code))
        activities = aims.Activity.objects.all()
        activities_by_role = activities.filter(
            participating_organisations__organisation=organisation
        ).distinct()
        activities_statuses = charts.activity_statuses_total(
            activities_by_role, organisation)
        return JsonResponse(activities_statuses, safe=False)


class DonorTransactionsByYear(View):
    ''' returns transactions by year for a given donor'''

    def get(self, *args, **kwargs):
        donor_code = self.kwargs['iati_identifier'] if 'iati_identifier' in kwargs else '0'

        organisation = get_object_or_404(
            aims.Organisation.objects, code=unquote(donor_code))
        activities = aims.Activity.objects.filter(
            participating_organisations__organisation=organisation
        ).distinct()
        activity_statuses = aims.ActivityStatus.objects.all()
        transactions_by_year = charts.transactions_by_year(
            activities, organisation, activity_statuses, json=False)
        return JsonResponse(transactions_by_year, safe=False)


class DonorActivities(View):
    ''' returns activities for a given donor'''

    def get(self, request, *args, **kwargs):
        donor_code = self.kwargs['iati_identifier'] if 'iati_identifier' in kwargs else '0'

        organisation = get_object_or_404(
            aims.Organisation.objects, code=unquote(donor_code))
        editor = base_utils.check_editor_privilege(self.request.user, organisation)

        activity_statuses = list(aims.ActivityStatus.objects.values('name'))
        organisation_roles = list(aims.OrganisationRole.objects.exclude(code='Accountable').values('name'))
        activity_queryset = aims.Activity.objects.filter(
            Q(participating_organisations__organisation=organisation) |
            Q(reporting_organisation=organisation) |
            Q(transaction__provider_organisation=organisation))\
            .distinct()\
            .prefetch_related('title_set', 'description_set')

        activities = {}
        for activity in activity_queryset.values('pk', 'start_planned', 'end_planned',
                                                 'activity_status__code', 'activity_status__name', 'openly_status',
                                                 'reporting_organisation_id', 'reporting_organisation__name'):
            activities[activity['pk']] = activity
            if activity['start_planned']:
                activity['start_planned'] = activity['start_planned'].strftime(DATE_FORMAT)
            if activity['end_planned']:
                activity['end_planned'] = activity['end_planned'].strftime(DATE_FORMAT)
            activity['title'] = ''
            activity['can_edit'] = editor and activity['reporting_organisation_id'] == organisation.pk
            activity['committed'] = 0
            activity['disbursed'] = 0
            activity['roles'] = {}
            activity['sectors'] = []
            activity['locations'] = []

        for activity in activity_queryset:
            activities[activity.pk]['title'] = activity.title
            activities[activity.pk]['description'] = activity.general_description

        sectors = aims.ActivitySector.objects.filter(activity_id__in=list(activities.keys())).values('activity_id', 'sector__name')
        for sector in sectors:
            activity = activities[sector['activity_id']]
            activity['sectors'].append(sector['sector__name'])

        locations = aims.Location.objects.filter(activity_id__in=list(activities.keys())).values('activity_id', 'name')
        for location in locations:
            activity = activities[location['activity_id']]
            activity['locations'].append(location['name'])

        transactions = aims.Transaction.objects.filter(activity_id__in=list(activities.keys())).values('activity_id', 'transaction_type_id', 'usd_value')
        for trans in transactions:
            trans_usd_value = trans['usd_value'] or 0
            activity = activities[trans['activity_id']]
            # committed and disbursed only include activities where the org is reporting, participating is excluded
            # see https://github.com/catalpainternational/openly/issues/396
            if trans['transaction_type_id'] == 'C' and activity['reporting_organisation_id'] == organisation.pk:
                activity['committed'] += trans_usd_value
            if trans['transaction_type_id'] == 'D' and activity['reporting_organisation_id'] == organisation.pk:
                activity['disbursed'] += trans_usd_value

        participating_orgs = aims.ActivityParticipatingOrganisation.objects.filter(activity_id__in=list(activities.keys())).values('activity_id', 'role_id', 'organisation__name')
        for org in participating_orgs:
            activity = activities[org['activity_id']]
            if org['organisation__name'] == organisation.name:
                activity['roles'][org['role_id']] = 1
            if org['role_id'] == 'Implementing':
                activity['implementing_partner'] = org['organisation__name']

        results = []
        for result in aims.Result.objects.filter(activity_id__in=list(activities.keys())).prefetch_related('resulttitle__narratives', 'resultdescription__narratives'):
            results.append(dict(activity_id=result.activity_id, title=result.title, description=result.description, activity_title=activities[result.activity_id].title))

        total_committed = 0
        total_disbursed = 0
        for activity in activities.values():
            activity['committed_pretty'] = base_utils.prettify_compact(activity['committed'])
            activity['disbursed_pretty'] = base_utils.prettify_compact(activity['disbursed'])
            activity['percent_disbursed'] = round(charts.percent_disbursed(activity['committed'], activity['disbursed']), 2)
            total_committed += activity['committed']
            total_disbursed += activity['disbursed']

        response_content = {}
        response_content['total_committed'] = base_utils.prettify_compact(total_committed)
        response_content['total_disbursed'] = base_utils.prettify_compact(total_disbursed)
        response_content['activities'] = list(activities.values())
        response_content['results'] = list(results)
        response_content['status_filters'] = activity_statuses
        response_content['role_filters'] = organisation_roles
        return JsonResponse(response_content)


class PersonView(TemplateView):
    template_name = 'profiles/person.html'

    def get(self, *args, **kwargs):
        person = get_object_or_404(Person, pk=kwargs['pk'])
        context = super(PersonView, self).get_context_data()
        organisation = person.organisation_profile.organisation
        editor = True if self.request.user.is_authenticated()\
            and (self.request.user.is_staff or
                 self.request.user.userorganisation.organisations.filter(pk=organisation.pk))\
            else False
        person.editor = editor
        context['person'] = person
        return self.render_to_response(context)


class ContactView(TemplateView):
    template_name = 'profiles/contact.html'

    def get(self, *args, **kwargs):
        contact = get_object_or_404(Contact, pk=kwargs['pk'])
        context = super(ContactView, self).get_context_data()
        context['contact'] = contact
        return self.render_to_response(context)


class PersonData(View):

    def get(self, *args, **kwargs):
        person = get_object_or_404(Person, pk=kwargs['pk'])
        personjson = serialize('json', [person])
        personjson = personjson.strip("[]")
        return JsonResponse(json)


class DeletePerson(View):

    def get(self, *args, **kwargs):
        person = Person.objects.get(pk=kwargs['pk'])
        data = {}
        try:
            person.delete()
            data['status'] = 1
        except Exception:
            data['status'] = 0
        return JsonResponse(data)


class ReorderPeople(View):

    def get(self, *args, **kwargs):
        people = self.request.GET.getlist('people[]')
        with transaction.atomic():
            for idx, person in enumerate(people):
                person_object = get_object_or_404(Person, pk=person)
                person_object.order = idx
                person_object.save()
        return JsonResponse('{success:true}')


class AjaxableResponseMixin(object):

    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class SaveContact(AjaxableResponseMixin, UpdateView):
    form_class = ContactForm
    model = Contact

    def get_success_url(self):
        return "/profile/donor/%s/" % self.object.organisation_profile.organisation.code


class CreatePerson(AjaxableResponseMixin, CreateView):
    template_name = "profiles/donor.html"
    form_class = PersonForm
    model = Person

    def get_success_url(self):
        return "/profile/donor/%s/" % self.object.organisation_profile.organisation.code


class UpdatePerson(AjaxableResponseMixin, UpdateView):
    template_name = "profiles/donor.html"
    form_class = PersonForm
    model = Person

    def get_success_url(self):
        return "/profile/donor/%s/" % self.object.organisation_profile.organisation.code


class RiotTagView(TemplateView):
    ''' renders a riot tag definition file '''

    def get_template_names(self):
        return "riottags/{tagfile}.html".format(tagfile=self.kwargs['tags'])
