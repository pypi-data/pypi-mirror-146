import json
from datetime import datetime
from typing import Dict, List
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.urls import reverse
from django.db.models import Count, F, Q, Max
from django.db.models.expressions import RawSQL
from django.db import transaction
from django.apps import apps

from django.http import (
    Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.base import RedirectView
from django.views.decorators.csrf import csrf_protect, requires_csrf_token

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from oipa import services as oipa_api
from oipa import serializers as oipa_serializers

from aims import models as aims, common_text
from iati_codelists import models as iati_codelists
from aims.api_serializers import serializers, editor as editor_serializers
from aims.api_serializers.formdata_serializer import AlwaysListViewSet
from aims.api_serializers import results_serializers
from aims.api_serializers.results_serializers import ResultSerializer
from aims.compare import activity_differences
from geodata.models import Adm1Region, Adm2Region
from simple_locations.models import Area

from .permissions import ActivityPermission, user_is_admin_or_superuser
PUBLISH_WARNING_MESSAGES = {
    'title': _("Add an activity title"),
    'description': _("Add an activity description"),
    'dates': _("Add a start date"),
    'status': _("Add an activity status"),
    'sector': _("Add a related sector"),
    'location': _("Add a related location"),
    'transaction': _("Add a transaction of type 'Commitment'"),
}


def get_activity_or_404(activity_pk):
    try:
        return aims.Activity.objects.all_openly_statuses().get(id=activity_pk)
    except aims.Activity.DoesNotExist:
        raise Http404()


class ActivityLog(APIView):
    """ Used by the review tab to GET a log of the activity changes, and to POST new comments. """
    permission_classes = [permissions.IsAuthenticated]

    def check_activity_permission(self, request, activity_pk):
        activity = get_activity_or_404(activity_pk)

        if not ActivityPermission().has_object_permission(request, None, activity):
            raise PermissionDenied()

    @staticmethod
    def etag_function(request, activity_pk=None):
        if activity_pk is None:
            return None
        # In case you were wondering, this will also work if there are no log messages for the activity
        last_log_message_time = aims.ActivityLogmessage.objects.filter(activity_id=activity_pk)\
            .aggregate(Max('tstamp'))['tstamp__max']
        return str(hash(last_log_message_time))

    def get(self, request, activity_pk=None):
        self.check_activity_permission(request, activity_pk)
        activitylogmessages = serializers.ActivityLogmessageSerializer(
            aims.ActivityLogmessage.objects.filter(
                activity_id=activity_pk
            ).order_by("-tstamp"), many=True
        ).data
        return JsonResponse({'activitylogmessages': activitylogmessages})

    def post(self, request, activity_pk=None):
        """ Used for POSTing new comments. Other activity logs are saved when the user takes actions. """
        self.check_activity_permission(request, activity_pk)

        log_type = request.data.get('type', None)
        if log_type != 'comment':
            raise ValidationError(detail='You can only create a log with {"type": "comment"}')

        comment = request.data.get('comment', None)
        if not comment:
            raise ValidationError(detail='You should supply a non-null comment')

        log_message = aims.ActivityLogmessage.objects.create(
            activity_id=activity_pk, body={'type': 'comment', 'comment': comment, 'uid': request.user.id}
        )
        # `objects.get` the instance ensures we have a Manager decorated instance
        return JsonResponse(serializers.ActivityLogmessageSerializer(
            aims.ActivityLogmessage.objects.get(pk=log_message.pk)
        ).data)


@api_view(['GET'])
def get_activity_publish_errors(request, activity_pk):
    activity = aims.Activity.objects.all_openly_statuses().get(id=activity_pk)
    if not ActivityPermission().has_object_permission(request, None, activity):
        raise PermissionDenied()

    return Response(activity.publish_errors)


class ActivitiesForReview(LoginRequiredMixin, TemplateView):
    template_name = 'editor/activities_for_review.html'

    def get_context_data(self, **kwargs):
        context = super(ActivitiesForReview, self).get_context_data(**kwargs)
        context['page_title'] = _('Activities for Review')

        organisation = self.organisation
        context['activities'] = json.dumps([{
            'pk': a.pk,
            'title': a.title,
            'reporting_organisation': a.reporting_organisation.name,
            'date_submitted': str(a.submitted_for_review_timestamp),
            'endorsed': a.endorsement_status if organisation.is_admin else a.is_endorsed_by(organisation)
        } for a in organisation.activities_for_review])
        return context

    def get(self, request, *args, **kwargs):
        self.organisation = get_object_or_404(aims.Organisation, pk=kwargs['organisation_pk'])

        user = self.request.user
        if not (user.is_superuser or user.organisation.is_admin or user.organisation.code == self.organisation.code):
            raise PermissionDenied()

        return super(ActivitiesForReview, self).get(request, *args, **kwargs)


class OrganisationActivityManager(LoginRequiredMixin, ListView):
    """ Shows all activities of the given organisation """

    template_name = 'editor/activity_manager.html'
    model = aims.Activity
    queryset = aims.Activity.objects.all_openly_statuses().filter(
        openly_status__in=[aims.StatusEnabledLocalData.OPENLY_STATUS_PUBLISHED,
                           aims.StatusEnabledLocalData.OPENLY_STATUS_DRAFT,
                           aims.StatusEnabledLocalData.OPENLY_STATUS_REVIEW,
                           aims.StatusEnabledLocalData.OPENLY_STATUS_IATIXML])

    @method_decorator(requires_csrf_token)
    def dispatch(self, *args, **kwargs):
        return super(OrganisationActivityManager, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        """ Adds get organisation functionality to base """

        try:
            self.organisation = aims.Organisation.objects.get(pk=kwargs['org_id'])
        except KeyError:
            return HttpResponseBadRequest()
        except aims.Organisation.DoesNotExist:
            return HttpResponseNotFound()

        return super(OrganisationActivityManager, self).get(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """ filter querset by organisation """

        select_relateds = ['reporting_organisation', 'activity_status', 'default_flow_type', 'default_finance_type', 'commitmenttotal']
        if 'oipa' in settings.INSTALLED_APPS:
            select_relateds += ['oipaactivitylink']

        return super(OrganisationActivityManager, self).get_queryset(*args, **kwargs).filter(reporting_organisation_id=self.organisation.pk).order_by('-last_updated_datetime')\
            .annotate(Count('transaction', distinct=True), Count('budget', distinct=True))\
            .select_related(*select_relateds)\
            .prefetch_related('sector', 'title_set', 'location_set', 'description_set', 'participating_organisations', 'results',)

    def get_context_data(self, *args, **kwargs):
        """ Adds additional context variables """

        context = super(OrganisationActivityManager, self).get_context_data(*args, **kwargs)
        context['project_name'] = getattr(settings, 'PROJECT_NAME', "")
        context['draft_status'] = aims.Activity.OPENLY_STATUS_DRAFT
        context['published_status'] = aims.Activity.OPENLY_STATUS_PUBLISHED
        context['iati_xml_status'] = aims.Activity.OPENLY_STATUS_IATIXML
        context['openly_statuses'] = dict([(status[0], str(status[1])) for status in aims.Activity.OPENLY_STATUSES])
        context['activity_statuses'] = aims.ActivityStatus.objects.order_by('order', 'code').values('code', 'name')
        context['organisation'] = self.organisation
        if hasattr(self, 'organisation') and self.organisation.can_create_activity(self.request.user):
            context['organisation_code'] = self.organisation.code
        elif self.request.user.organisation:
            context['organisation_code'] = self.request.user.organisation.code
        else:
            raise PermissionDenied

        context['local_iati_identifiers'] = set()
        context['total_published'] = 0
        context['total_drafts'] = 0
        context['total_transactions'] = 0
        context['budgets_count'] = 0
        context['compare_details'] = {}
        context['incomplete_activities'] = 0
        context['implementing_ending_soon'] = 0
        context['total_iati_linked'] = 0

        iati_sync_enabled = getattr(settings, 'OIPA_SYNC_ENABLED', False)
        context['iati_tab_accessable'] = False
        if self.request.user.is_superuser or self.request.user.organisation and self.request.user.organisation.iati_sync_enabled:
            context['iati_tab_accessable'] = True

        local_iati_ids = {}
        xml_iati_ids = {}
        completions = []

        # calcualte and set next quarter's start/end dates
        current_date = datetime.now()
        nextQuarter = int((current_date.month - 1) / 3 + 1) % 4 + 1
        context['next_quarter_int'] = nextQuarter
        next_qtr_start = datetime(current_date.year, 3 * nextQuarter - 2, 1).date()
        next_qtr_end = next_qtr_start + relativedelta(months=3, days=-1)

        for activity in context['object_list']:
            # return count of implementing activities with planned end dates falling within the next quarter
            if activity.activity_status_id == 2 and activity.end_planned and (activity.end_planned <= next_qtr_end and activity.end_planned >= next_qtr_start):
                context['implementing_ending_soon'] += 1
            # return count of activities linked to IATI
            if iati_sync_enabled and activity.iati_sync_enabled:
                context['total_iati_linked'] += 1
            if activity.openly_status != aims.Activity.OPENLY_STATUS_IATIXML:
                context['local_iati_identifiers'].add(activity.iati_identifier)
                if activity.openly_status == aims.Activity.OPENLY_STATUS_PUBLISHED:
                    context['total_published'] += 1
                    if activity.completion is None:
                        # trigger the signal that sets the activity completion
                        activity.save()
                    if (activity.completion or 0) < 1:
                        context['incomplete_activities'] += 1
                if activity.openly_status == aims.Activity.OPENLY_STATUS_DRAFT:
                    context['total_drafts'] += 1

                context['total_transactions'] += activity.transaction__count
                context['budgets_count'] += activity.budget__count

                local_iati_ids[activity.iati_identifier] = activity.pk
                if activity.iati_identifier in xml_iati_ids:
                    context['compare_details'][activity.pk] = {'local': activity.pk, 'xml': xml_iati_ids[activity.iati_identifier]}

                if activity.completion:
                    completions.append(activity.completion)

            else:
                xml_iati_ids[activity.iati_identifier] = activity.pk
                if activity.iati_identifier in local_iati_ids:
                    context['compare_details'][local_iati_ids[activity.iati_identifier]] = {'local': local_iati_ids[activity.iati_identifier], 'xml': activity.pk}

        context['avg_completion'] = (sum(completions) / len(completions)) if len(completions) > 0 else 0

        return context


class OrganisationActivityWithoutFinancialsManager(OrganisationActivityManager):
    """ Shows all activities of the given organisation """
    template_name = 'editor/activity_manager_without_financials.html'


class IatiActivity(LoginRequiredMixin, TemplateView):
    template_name = 'editor/iati_activity.html'


class ChooseOrganisation(LoginRequiredMixin, TemplateView):
    """ Lets a user choose an organistion to associate with an activity they want to create. """
    template_name = "editor/choose_organisation.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ChooseOrganisation, self).get_context_data(*args, **kwargs)
        # Show all orgs to superusers or admins
        if user_is_admin_or_superuser(self.request.user):
            organisations = aims.Organisation.objects.filter(type__isnull=False)
        else:
            organisations = self.request.user.organisations
        context['organisations'] = organisations
        context['page_title'] = _('Choose organisation')
        return context


class CreateActivity(LoginRequiredMixin, RedirectView):
    permanent = False

    def check_permissions(self, organisation):
        """ Raise a 403 if the user does not have the permission to update the organisation. """
        user = self.request.user
        if user_is_admin_or_superuser(user):
            return True
        try:
            if organisation.code not in user.userorganisation.organisations.values_list('code', flat=True):
                raise PermissionDenied
        except aims.UserOrganisation.DoesNotExist:
            raise PermissionDenied

    def post_activity_create(self, activity: aims.Activity) -> None:
        """
        Additional processing of the activity before
        redirecting the user to the editor can be performed
        here. The initial use case is to pre populate the Location
        selection with an area a User in Dird is responsible for
        """
        return

    def get_redirect_url(self, *args, **kwargs):
        """ Create an activity, then redirect to the edit_activity view. """
        serializer = kwargs.get('serializer', serializers.ActivityDeserializer)
        organisation = get_object_or_404(aims.Organisation, code=kwargs['organisation_id'])
        self.check_permissions(organisation)
        serialized_activity = serializer(
            data={'reporting_organisation': {'code': organisation.code}}, editor_creation=True)
        serialized_activity.is_valid()
        with transaction.atomic():
            created_activity = serialized_activity.save()
            aims.ActivityLogmessage.objects.create(activity=created_activity,
                                                   body={'type': 'creation', 'uid': self.request.user.id})
            self.post_activity_create(created_activity)
        return reverse('edit_activity', kwargs={'pk': created_activity.pk})


class EditActivity(LoginRequiredMixin, DetailView):
    template_name = "editor/edit_data.html"
    model = aims.Activity
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        ''' overwrite get to allow redirect if activity is IATIXML'''
        self.object = self.get_object()

        if self.object and self.object.openly_status == aims.Activity.OPENLY_STATUS_IATIXML:
            return HttpResponseRedirect(reverse('iati_activity', kwargs={'pk': self.object.pk}))

        return super(EditActivity, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        activity = get_activity_or_404(self.kwargs['pk'])

        if not ActivityPermission().has_object_permission(self.request, None, activity):
            raise PermissionDenied()

        return activity

    def get_success_url(self):
        return reverse('edit_activity', args=(self.object.pk,))

    def activity_budgets_are_quarterly(self):
        """
        Check whether activity budgets are
        all exactly one quarter in length
        """
        budgets = self.object.budget_set.annotate(
            startDate=RawSQL("SELECT EXTRACT (DAY FROM period_start)", ''),
            startMonth=RawSQL("SELECT EXTRACT (MONTH FROM period_start)", ''),
            endOfPeriod=RawSQL("SELECT period_start + interval '3 months' - interval '1 day'", '')
        ).exclude(
            startDate=1,
            startMonth__in=[1, 4, 7, 10],
            period_end=F('endOfPeriod')
        )
        return budgets.count() == 0

    def get_context_data(self, *args, **kwargs):

        def render_dict(data):
            renderer = JSONRenderer()
            return renderer.render(data)

        def safe(data):
            return mark_safe(render_dict(data).decode('utf-8'))

        data = {}
        if getattr(settings, 'EDITOR_HAS_FINANCIALS', True):
            self.object.transaction_set.update_usd_value()
            data['transactions'] = editor_serializers.TransactionSerializer(instance=self.object.transaction_set, many=True).data

        context = super(EditActivity, self).get_context_data(*args, **kwargs)
        user = self.request.user

        context['data'] = safe(data)
        context['user_organisation_code'] = user.organisation.code if user.organisation else None

        organisation = context['activity'].reporting_organisation
        context['organisation'] = organisation
        if organisation.can_create_activity(self.request.user):
            context['organisation_code'] = organisation.code
        else:
            context['organisation_code'] = self.request.user.organisation.code

        if context['activity'].title:
            context['page_title'] = _('Edit {}: {}'.format(common_text.get('activity_or_program'), context['activity'].title))
        else:
            context['page_title'] = _('Edit {}'.format(common_text.get('activity_or_program')))
        context['project_name'] = getattr(settings, 'PROJECT_NAME', "")
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
        try:
            context['site_name'] = settings.OPENLY_SITE_CONTEXT['site_name']
        except (KeyError, AttributeError):
            context['site_name'] = 'openly'

        data = {
            'activity': serializers.ActivityDeserializer(instance=self.object).data,
            'results': dict(
                # Results and related objects for this Activity
                result=ResultSerializer(self.object.results.all(), many=True).data,
                resulttitle=results_serializers.ResultTitleSerializer(
                    aims.ResultTitle.objects.filter(result__activity=self.object), many=True).data,
                resultdescription=results_serializers.ResultDescriptionSerializer(
                    aims.ResultDescription.objects.filter(result__activity=self.object), many=True).data,
                resultindicator=results_serializers.ResultIndicatorSerializer(
                    aims.ResultIndicator.objects.filter(result__activity=self.object).prefetch_related('result', 'result__activity__reporting_organisation'), many=True).data,
                resultindicatortitle=results_serializers.ResultIndicatorTitleSerializer(
                    aims.ResultIndicatorTitle.objects.filter(result_indicator__result__activity=self.object), many=True).data,
                resultindicatorbaselinecomment=results_serializers.ResultIndicatorBaselineCommentSerializer(
                    aims.ResultIndicatorBaselineComment.objects.filter(result_indicator__result__activity=self.object),
                    many=True).data,
                resultindicatorkeyprogressstatement=results_serializers.ResultIndicatorKeyProgressStatementSerializer(
                    aims.ResultIndicatorKeyProgressStatement.objects.filter(result_indicator__result__activity=self.object),
                    many=True).data,
                resultindicatordescription=results_serializers.ResultIndicatorDescriptionSerializer(
                    aims.ResultIndicatorDescription.objects.filter(result_indicator__result__activity=self.object),
                    many=True).data,
                contenttype=ContentType.objects.filter(app_label='aims').values('id', 'app_label', 'model'),
                resulttype=iati_codelists.ResultType.objects.values('code', 'name', 'description'),
                resultindicatorperiod=results_serializers.ResultIndicatorPeriodSerializer(
                    aims.ResultIndicatorPeriod.objects.filter(result_indicator__result__activity=self.object), many=True).data,
                resultindicatortype=results_serializers.ResultIndicatorTypeSerializer(
                    aims.ResultIndicatorType.objects.filter(result_indicator__result__activity=self.object), many=True).data,

                resultindicatorperiodactualdimension=results_serializers.ResultIndicatorPeriodActualDimensionSerializer(
                    aims.ResultIndicatorPeriodActualDimension.objects.filter(result_indicator_period__result_indicator__result__activity=self.object), many=True).data,
            ),
            # For Narratives it is useful to know about Django's content types
            'narratives': results_serializers.NarrativeSerializer(aims.Narrative.objects.filter(activity=self.object), many=True).data,
            'contacts': editor_serializers.ContactSerializer(aims.ContactInfo.objects.filter(activity=self.object), many=True).data,
        }

        context['iati_tab_accessable'] = False
        if getattr(settings, 'EDITOR_HAS_FINANCIALS', True):
            data['transactions'] = editor_serializers.TransactionSerializer(aims.Transaction.objects.filter(activity=self.object), many=True).data
            data['budgets'] = editor_serializers.BudgetQuarterSerializer(
                aims.Budget.objects.filter(activity=self.object),
                many=True).data

            if self.request.user.is_superuser or self.request.user.organisation and self.request.user.organisation.iati_sync_enabled:
                context['iati_tab_accessable'] = True

            if getattr(settings, 'OIPA_SYNC_ENABLED', False):
                # Placeholder for IATI data to be replaced by JSON from AJAX request
                # prevent RiotJS template errors
                data['iati_data'] = {
                    'transactions': {
                        'B': {'clean_sum': 0, 'clean_count': 0, 'raw_count': 0, 'raw_sum': 0},
                        'C': {'clean_sum': 0, 'clean_count': 0, 'raw_count': 0, 'raw_sum': 0},
                        'IF': {'clean_sum': 0, 'clean_count': 0, 'raw_count': 0, 'raw_sum': 0},
                        'OF': {'clean_sum': 0, 'clean_count': 0, 'raw_count': 0, 'raw_sum': 0},
                    },
                    'validation_results': {
                        'B': False,
                        'C': False,
                        'IF': False,
                        'OF': False,
                    },
                    'link_info': oipa_serializers.OipaActivityLinkSerializer(oipa_api.ActivityLink(context['activity'].id).get_link()).data,
                    'sync_records': oipa_api.get_syncs(context['activity'].id)
                }

        if 'dird_templates' in settings.INSTALLED_APPS:
            model_name_to_context = {'ActivityFinances': 'dird_finances', 'ActivityCompliance': 'dird_compliance'}
            for model_name, context_key in model_name_to_context.items():
                model = apps.get_model('dird_templates', model_name)
                field_names = [field.name for field in model._meta.fields if field.name != 'activity']
                instance = model.objects.get_or_create(activity=context['activity'])[0]
                context[context_key] = {
                    field: getattr(instance, field) for field in field_names
                }

            model = apps.get_model('dird_templates', 'ActivityStatus')
            status_instance = model.objects.get_or_create(activity=context['activity'])[0]
            context['dird_project_completion'] = {
                'status': getattr(status_instance, 'activity').activity_status.code if getattr(status_instance, 'activity').activity_status is not None else None,
                'completion_status': getattr(status_instance, 'completion_status')
            }

        context['data'] = safe(data)

        templates = dict(
            transaction=serializers.TransactionDeserializer().data,
            budget=serializers.BudgetDeserializer().data,
            resultindicator=dict(result=None, measure="1", ascending=True, baseline_year=2017, baseline_value=0),
            indicatormeasure=results_serializers.IndicatorMeasureSerializer().data,
            narrative=results_serializers.NarrativeSerializer().data,
            resultindicatorperiod=dict(result_indicator=None, period_start='2017-01-01', period_end='2017-12-31', target=0, actual=0),
            resultindicatortype=dict(result=None, display='Narrative', sector='Multi-sectoral', target='')
        )
        context['templates'] = safe(templates)

        if getattr(settings, 'EDITOR_HAS_DOCUMENTS_TAB', True):
            context['documents'] = safe(serializers.DocumentSerializer(self.object.documentlink_set.all(), many=True).data)

        context['model_choices'] = safe(self.model_choices)
        context['languages'] = safe({k: {'language_name': v} for (k, v) in settings.LANGUAGES})

        if getattr(settings, 'ENDORSEMENT_ENABLED', False):
            try:
                context['admin_organisation_name'] = aims.Organisation.objects.get(is_admin=True).name
            except aims.Organisation.DoesNotExist:
                context['admin_organisation_name'] = 'No admin organisation'
            context['endorsements'] = json.dumps(context['activity'].get_endorsements())
        context['is_admin_or_superuser'] = user_is_admin_or_superuser(user)
        context['budgets_are_quarterly'] = self.activity_budgets_are_quarterly()
        # allow individual projects to override the General/Finances tabs
        context['EDITOR_GENERAL_TAB'.lower()] = getattr(settings, 'EDITOR_GENERAL_TAB', 'tags/tab-general.html')
        context['editor_custom_finances_tab'] = getattr(settings, 'EDITOR_FINANCES_TAB', None)

        if getattr(settings, 'EDITOR_HAS_MSDP', False):
            # The Activitytags implementation for Projectbank. These choices are loaded
            # using the (Django 1.1+) recommended '|json_script' filter method.
            context['msdp'] = {
                'tags': {t.pop('pk'): t for t in aims.Tag.objects.filter(vocabulary=10).values('pk', 'name').order_by('pk')},
                'goals': {
                    "1": {"title": "Pillar 1, Goal 1: Peace, National Reconciliation, Security & Good Governance"},
                    "2": {"title": "Pillar 1, Goal 2: Economic Stability & Strengthened Macroeconomic Management"},
                    "3": {"title": "Pillar 2, Goal 3: Job Creation & Private Sector Led Growth"},
                    "4": {"title": "Pillar 3, Goal 4: Human Resources & Social Development for a 21st Century Society"},
                    "5": {"title": "Pillar 3, Goal 5: Natural Resources & the Environment for Posterity of the Nation"}
                },
            }
        return context

    @property
    def model_choices(self):
        """
        Returns a dictionary choice name -> choices.
        Each choice is a tuple
         [0]: db_value
         [1]: human_value
         [2]: group name (optional)
         [3]: search string (optional)
        """
        choices = {}
        # handle simple models where value = code and human display = name
        common_currencies = set(
            list(
                aims.Transaction.objects.distinct('currency_id').values_list('currency_id', flat=True)) +
            list(
                aims.Budget.objects.distinct('currency_id').values_list('currency_id', flat=True)
            )
        )

        if hasattr(settings, 'EDITOR_HAS_IGA'):
            #  For editors which want to select organisation from parents, we use this to find parent
            choices['organisation_parent'] = list(aims.Organisation.objects.filter(type=100, parent__isnull=False).values_list('pk', 'parent'))
            choices['organisation_region_govt'] = list(aims.Organisation.objects.filter(type=100).filter(Q(code__endswith='RG') | Q(code__endswith='SG')).order_by('name').values_list('pk', flat=True))
            choices['organisation_donors'] = [(obj.code, obj.name, None, obj.abbreviation) for obj in aims.Organisation.objects.filter(type__name='Donor')]

        choice_name_to_queryset = {
            'activity_status': aims.ActivityStatus.objects.order_by('order', 'code'),
            'collaboration_type': 'CollaborationType',
            'dac_3s': aims.IATISector.objects.filter(code=F('category_id')),
            # dac_5s have a 5 digit code, hence the filtering on code__gt
            'dac_5s': aims.IATISector.objects.filter(category__isnull=False, code__gt=9999),
            'sector_working_group': 'NationalSector',
            'policy_marker': 'PolicyMarker',
            'flow_type': 'FlowType',
            'tied_status': 'TiedStatus',
            'currency': aims.Currency.objects.all().order_by('name'),
            'common_currency': aims.Currency.objects.filter(code__in=common_currencies),
            'transaction_type': 'TransactionType',
            'disbursement_channel': 'DisbursementChannel',
            'budget_type': 'BudgetType',
            'budget_status': 'BudgetStatus',
            'significance': 'PolicySignificance',
            'contact_type': 'ContactType',
            'file_format': 'FileFormat',
            'document_category': 'DocumentCategory',
            'language': 'Language',
            'type': iati_codelists.ResultType.objects.all(),
            'indicatormeasure': iati_codelists.IndicatorMeasure.objects.all(),
        }

        if settings.PROJECT_NAME == _('Project Bank'):
            choice_name_to_queryset['funding_sources'] = apps.get_model('pb_profile', 'FundingSource').objects.all()

        for choice_name, queryset in choice_name_to_queryset.items():
            if isinstance(queryset, str):
                queryset = getattr(aims, queryset).objects.all().order_by('pk')
            choices[choice_name] = [(obj.code, obj.name) for obj in queryset]

        organisations = aims.Organisation.objects.exclude(name='')
        # See GitHub issue #1670 - Exclude "Multiple Donors"
        if aims.ActivityParticipatingOrganisation.objects.filter(activity=self, organisation__name='Multiple Donors').count() == 0:
            organisations = organisations.exclude(name='Multiple Donors')

        choices['organisation'] = [(obj.code, obj.name, None, obj.abbreviation) for obj in organisations.order_by('name')]
        choices['aid_type'] = [(obj.code, obj.name, obj.category.name) for obj in aims.AidType.objects.select_related('category').all()]
        choices['finance_type'] = [(obj.code, obj.name, obj.category.name.capitalize()) for obj in aims.FinanceType.objects.select_related('category').all()]
        choices['transaction_type'] = serializers.TransactionTypeSerializer(serializers.TransactionTypeSerializer.Meta.model.objects.all(), many=True).data
        choices['activity'] = [(obj.pk, obj.title) for obj in aims.Activity.objects.prefetch_related('title_set').all()]
        choices['indicatormeasure'] = [(obj.code, obj.name) for obj in iati_codelists.IndicatorMeasure.objects.all()]
        choices['result_type'] = iati_codelists.ResultType.objects.values('code', 'name', 'description'),

        choices['locations'] = self.location_choices()
        choices['transaction_type'] = serializers.TransactionTypeSerializer(serializers.TransactionTypeSerializer.Meta.model.objects.all(), many=True).data

        # Additional choices for ResultIndicatorType
        choices['resultindicatortype_display'] = aims.ResultIndicatorType.display_choices
        choices['resultindicatortype_sector'] = aims.ResultIndicatorType.sector_choices
        choices['activity_date_level_of_detail'] = aims.Activity.DateDetailChoices.choices
        choices['required_to_publish'] = getattr(settings, 'REQUIRED_TO_PUBLISH', aims.openly_required_to_publish)

        if 'dird_templates' in settings.INSTALLED_APPS:
            # Additional simplified Sectors choice for DIRD
            choices['sectors'] = [(obj.code, obj.name) for obj in aims.Sector.objects.all()]
            # Expenditure categories on the DIRD expenditures tab
            ExpenditureCategory = apps.get_model('dird_templates', 'ExpenditureCategory')
            choices['expenditure_category'] = ExpenditureCategory.objects.all().values('pk', 'name')
            choices['expenditure_payment_status'] = apps.get_model('dird_templates', 'Expenditure').PAYMENT_STATUS_CHOICES.choices

            # DIRD Expenditure compliance fields
            # Expenditure fields with "Yes", "No", "NA" choices
            # are choice'd into a tuple of 'name', 'help_text'
            Expenditure = apps.get_model('dird_templates', 'Expenditure')
            choices['expenditure_compliance_fields'] = map(lambda c: (c.name, c.help_text), filter(lambda i: i.choices == Expenditure.ComplianceChoice.choices, Expenditure._meta.fields))
            choices['expenditure_compliance_field_choices'] = Expenditure.ComplianceChoice.choices
            choices['expenditure_project_payment_stage_choices'] = Expenditure.ProjectPaymentStage.choices

        return choices

    def location_choices(self):
        """
        Returns the choices list for locations. The first element of each tuple is a primary key.
        Primary keys are distinct among Adm1Region and Adm2Region, so there is no risk of conflict

        Several versions of "area serialization" are used in different versions of openly.
        Some use 'simple_locations' areas, some use 'ADM1' type regions
        """

        simple_locations = getattr(settings, 'USE_SIMPLE_LOCATIONS', False)
        has_financials = getattr(settings, 'EDITOR_HAS_FINANCIALS', False)
        custom_finances = getattr(settings, 'EDITOR_FINANCES_TAB', False)

        if not simple_locations:
            # Mohinga
            return get_admregion_choices()

        if not has_financials or custom_finances:
            # Project Bank, Hamutuk
            return location_choices_nofinancials()

        # Plov
        return get_simple_location_choices()


def get_admregion_choices():
    """
    The "original" location serializer as used in mohinga uses Adm1 and Adm2 regions
    """
    regions = Adm1Region.objects.values('adm1_code', 'name')
    subregions = Adm2Region.objects.values('code', 'name', 'region_id')
    locations = [{'text': _('Nationwide'), 'value': settings.ROOT_COUNTRY_CODE}]
    for region in regions:
        serialized_region = {
            'text': region['name'],
            'choices': [{'text': _('all subregions of ') + region['name'], 'value': region['adm1_code']}],
        }
        relevant_subregions = [sr for sr in subregions if sr['region_id'] == region['adm1_code']]
        for subregion in relevant_subregions:
            serialized_region['choices'].append({'value': subregion['code'], 'text': subregion['name']})
        locations.append(serialized_region)
    return locations


def get_simple_location_choices():
    locations = []
    lookup = {}
    for area in Area.objects.get(code=settings.ROOT_COUNTRY_CODE).get_family().values('name', 'id', 'parent_id', 'level').order_by('level', 'name'):
        if area['level'] == 0:
            locations = [{'text': area['name'], 'value': area['id']}]
        elif area['level'] == 1:
            region = {
                'text': area['name'],
                'choices': [{'text': _('all subregions of {area}').format(area=area['name']), 'value': area['id']}],
            }
            locations.append(region)
            lookup[area['id']] = region
        elif area['level'] == 2:
            region = lookup[area['parent_id']]
            region['choices'].append({'value': area['id'], 'text': area['name']})
    return locations


def location_choices_nofinancials():
    """ Returns the choices list for locations. The first element of each tuple is a primary key.
    """
    area_choices = []
    full_area_names_by_pk = {}
    if hasattr(settings, 'FOCUS_AREA_ID'):
        focus_areas = Area.objects.get(pk=settings.FOCUS_AREA_ID).get_descendants(include_self=True).values_list('pk', flat=True)
    elif hasattr(settings, 'ROOT_COUNTRY_CODE'):
        focus_areas = Area.objects.get(code=settings.ROOT_COUNTRY_CODE).get_descendants().values_list('pk', flat=True)
    else:
        raise AssertionError('No top level area')
    for area in Area.objects.filter((Q(level__gte=1) & Q(level__lte=2)) | Q(pk__in=focus_areas)).values('pk', 'kind_id', 'kind__name', 'name', 'parent_id'):
        full_name = area['kind__name'] + ' ' + area['name']
        if area['parent_id'] is None or area['parent_id'] not in full_area_names_by_pk:
            full_area_names_by_pk[area['pk']] = full_name
        else:
            parent_full_name = full_area_names_by_pk[area['parent_id']]
            full_area_names_by_pk[area['pk']] = "{} | {}".format(parent_full_name, full_name)
        serialized_area = {
            'full_name': full_area_names_by_pk[area['pk']],
            'name': area['name'],
            'kind': area['kind__name'],
            'code': area['pk'],
            'parent': area['parent_id'],
        }
        area_choices.append(serialized_area)
    return area_choices


def user_can_edit(user=None, **kwargs):
    if user is None:
        return False
    if user.is_superuser:
        return True
    if user.organisation is not None and user.organisation.is_admin:
        return True
    if 'activity' in kwargs and isinstance(kwargs['activity'], aims.Activity):
        return user.userorganisation.organisations.filter(pk=kwargs['activity'].reporting_organisation_id).exists()
    if 'org_id' in kwargs:
        return user.userorganisation.organisations.filter(pk=kwargs['org_id']).exists()


class ImportActivityToLocal(LoginRequiredMixin, View):
    http_method_names = ['post']

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(ImportActivityToLocal, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            self.activity = aims.Activity.objects.iatixml().get(pk=kwargs['pk'])
            if not user_can_edit(self.request.user, activity=self.activity):
                return HttpResponseForbidden()
        except KeyError:
            return HttpResponseBadRequest()
        except aims.Activity.DoesNotExist:
            return HttpResponseNotFound()

        self.activity.openly_status = aims.Activity.OPENLY_STATUS_DRAFT
        self.activity.save()

        return HttpResponse("Activity is now draft")


class ImportActivityAll(LoginRequiredMixin, View):
    http_method_names = ['post']

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(ImportActivityAll, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            local_iati_identifiers = [activity.iati_identifier for activity in aims.Activity.objects.with_drafts()]
            if not user_can_edit(self.request.user, org_id=kwargs['org_id']):
                return HttpResponseForbidden()
            activities = aims.Activity.objects.iatixml().filter(reporting_organisation_id=kwargs['org_id'])\
                                                        .exclude(iati_identifier__in=local_iati_identifiers)
        except KeyError:
            return HttpResponseBadRequest()
        except aims.Organisation.DoesNotExist:
            return HttpResponseNotFound()

        activities.update(openly_status=aims.Activity.OPENLY_STATUS_DRAFT)
        return HttpResponse("OK")


class Localizations(object):
    ''' Holds localizations used in multiple places '''
    LEFT = _('left')
    RIGHT = _('right')
    ACTION_DESCRIPTION = _('You may replace the activity on the %(position_1)s with the %(status)s activity on the %(position_2)s')
    REPLACE = _('Import IATI')
    RESTORE = _('Restore Archived')
    KEEP_LOCAL = _('Keep Local')


class CompareActivities(LoginRequiredMixin, TemplateView):
    template_name = 'editor/compare_activities.html'

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CompareActivities, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CompareActivities, self).get_context_data(*args, **kwargs)
        try:
            left = aims.Activity.objects.all_openly_statuses().get(pk=kwargs['left'])
            right = aims.Activity.objects.all_openly_statuses().get(pk=kwargs['right'])
        except KeyError:
            raise AttributeError("Compare Activities view must be called with left and right activity keys")
        except aims.Activity.DoesNotExist:
            raise Http404(_("No Activity found matching the query"))

        context['page_title'] = _('Compare Activities')
        context['left'] = left
        context['right'] = right
        context['differences'] = activity_differences(left, right)
        context['openly_statuses'] = dict([(status[0], str(status[1])) for status in aims.Activity.OPENLY_STATUSES])
        if left.iati_identifier == right.iati_identifier:
            action = {}
            if left.openly_status == aims.Activity.OPENLY_STATUS_IATIXML and right.openly_status in [aims.Activity.OPENLY_STATUS_DRAFT, aims.Activity.OPENLY_STATUS_PUBLISHED]:
                # one activity is iati one is published or draft
                action['left_button_text'] = Localizations.REPLACE
                action['left_button_action'] = True
                action['right_button_text'] = Localizations.KEEP_LOCAL
                action['description'] = Localizations.ACTION_DESCRIPTION % {
                    'position_1': Localizations.RIGHT, 'position_2': Localizations.LEFT, 'status': aims.Activity.OPENLY_STATUS_IATIXML}
                action['url'] = reverse('replace', kwargs={'local': right.pk, 'remote': left.pk})
            elif left.openly_status in [aims.Activity.OPENLY_STATUS_PUBLISHED, aims.Activity.OPENLY_STATUS_DRAFT] and right.openly_status == aims.Activity.OPENLY_STATUS_IATIXML:
                # one activity is iati one is published or draft
                action['right_button_text'] = Localizations.REPLACE
                action['right_button_action'] = True
                action['left_button_text'] = Localizations.KEEP_LOCAL
                action['description'] = Localizations.ACTION_DESCRIPTION % {'position_1': Localizations.LEFT, 'position_2': Localizations.RIGHT, 'status': aims.Activity.OPENLY_STATUS_IATIXML}
                action['url'] = reverse('replace', kwargs={'local': left.pk, 'remote': right.pk})
            elif left.openly_status in [aims.Activity.OPENLY_STATUS_PUBLISHED, aims.Activity.OPENLY_STATUS_DRAFT] and right.openly_status == aims.Activity.OPENLY_STATUS_ARCHIVED:
                # one activity is archived one is published or draft
                action['right_button_text'] = Localizations.RESTORE
                action['right_button_action'] = True
                action['left_button_text'] = Localizations.KEEP_LOCAL
                action['description'] = Localizations.ACTION_DESCRIPTION % {
                    'position_1': _('right'), 'position_2': _('left'), 'status': aims.Activity.OPENLY_STATUS_ARCHIVED}
                action['url'] = reverse('restore', kwargs={'archived': right.pk, 'local': left.pk})
            elif left.openly_status == aims.Activity.OPENLY_STATUS_ARCHIVED and right.openly_status in [aims.Activity.OPENLY_STATUS_PUBLISHED, aims.Activity.OPENLY_STATUS_DRAFT]:
                # one activity is archived one is published or draft
                action['left_button_text'] = Localizations.RESTORE
                action['left_button_action'] = True
                action['right_button_text'] = Localizations.KEEP_LOCAL
                action['description'] = Localizations.ACTION_DESCRIPTION % {
                    'position_1': _('right'), 'position_2': _('left'), 'status': aims.Activity.OPENLY_STATUS_ARCHIVED}
                action['url'] = reverse('restore', kwargs={'archived': left.pk, 'local': right.pk})
            context['available_action'] = action
        return context


class ReplaceLocalWithIATI(LoginRequiredMixin, View):
    http_method_names = ['post']

    @method_decorator(csrf_protect)
    def post(self, *args, **kwargs):
        try:
            self.local_activity = aims.Activity.objects.with_drafts().get(pk=kwargs['local'])
            self.iati_activity = aims.Activity.objects.iatixml().get(pk=kwargs['remote'])
            if not user_can_edit(self.request.user, activity=self.iati_activity) or not user_can_edit(self.request.user, activity=self.local_activity):
                return HttpResponseForbidden()
        except KeyError:
            return HttpResponseBadRequest()
        except aims.Activity.DoesNotExist:
            return HttpResponseNotFound()

        self.iati_activity.openly_status = self.local_activity.openly_status
        self.local_activity.openly_status = aims.Activity.OPENLY_STATUS_ARCHIVED

        self.local_activity.save()
        self.iati_activity.save()

        return HttpResponseRedirect(reverse('compare', kwargs={'left': self.local_activity.pk, 'right': self.iati_activity.pk}))


class RestoreArchived(LoginRequiredMixin, View):
    http_method_names = ['post']

    @method_decorator(csrf_protect)
    def post(self, *args, **kwargs):
        try:
            self.archived_activity = aims.Activity.objects.archived().get(pk=kwargs['archived'])
            self.local_activity = aims.Activity.objects.with_drafts().get(pk=kwargs['local'])
            if not user_can_edit(self.request.user, activity=self.iati_activity) or not user_can_edit(self.request.user, activity=self.local_activity):
                return HttpResponseForbidden()
        except KeyError:
            return HttpResponseBadRequest()
        except aims.Activity.DoesNotExist:
            return HttpResponseNotFound()

        self.archived_activity.openly_status = self.local_activity.openly_status
        self.local_activity.openly_status = aims.Activity.OPENLY_STATUS_ARCHIVED

        self.local_activity.save()
        self.archived_activity.save()

        return HttpResponseRedirect(reverse('compare', kwargs={'left': self.local_activity.pk, 'right': self.iati_activity.pk}))


class ArchiveActivity(LoginRequiredMixin, View):
    http_method_names = ['post']

    @method_decorator(csrf_protect)
    def post(self, *args, **kwargs):
        try:
            self.activity = aims.Activity.objects.all_openly_statuses().get(pk=kwargs['pk'])
            if not user_can_edit(self.request.user, activity=self.activity):
                return HttpResponseForbidden()
        except KeyError:
            return HttpResponseBadRequest()
        except aims.Activity.DoesNotExist:
            return HttpResponseNotFound()

        self.activity.openly_status = aims.Activity.OPENLY_STATUS_ARCHIVED

        self.activity.save()

        if getattr(settings, 'ARCHIVE_ACTIVITY_REDIRECT', None):
            return HttpResponseRedirect(reverse(settings.ARCHIVE_ACTIVITY_REDIRECT))

        return HttpResponseRedirect(reverse('activity_manager', kwargs={'org_id': self.activity.reporting_organisation_id}))


class ActivityDependentsViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
    Used to PUT an activity and its dependent objects.
    Subclass this view and set the `serializer` class attribute.
    """
    queryset = aims.Activity.objects.editables().all()  # type: QuerySet
    permission_classes = (IsAuthenticated, ActivityPermission)


class ActivityLogmessageLogger(ActivityDependentsViewSet):

    # Mapping of identifying keys (as submitted to various serializers used by the activity editor) to tab names
    # Data definition:
    # unique_key_in_data_submitted_to_serializer = ['editortab_translatable_title_string', 'editortab_subtab_translatable_title_string_if_we_have_a_subtab']
    tabmap = dict(
        sectors=['Sectors'],
        results=['Results'],
        participating_organisations=['Organizations'],
        iati_identifier=['General'],
        locations=['Locations'],
        contactinfo_set=['Contacts'],
        default_aid_type=['Finances & Budgets', 'Default Settings'],
        transaction_set=['Finances & Budgets', 'Transactions'],
        budget_set=['Finances & Budgets', 'Budgets'],
    )  # type: Dict[str, List[str]]

    def create_activitylogmessage(self):
        if self.request.headers.get("X-Editor-Tab"):
            aims.ActivityLogmessage.from_editor_request(self.request, activity=self.kwargs["pk"])
        else:
            try:
                identifying_key = set(self.tabmap.keys()).intersection(self.request.data.keys()).pop()
            except KeyError:  # No identifying key in tabmap
                return
            aims.ActivityLogmessage.from_editor(
                activity=self.kwargs["pk"],
                tab=self.tabmap[identifying_key],
                user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        self.create_activitylogmessage()
        return super(ActivityLogmessageLogger, self).get_serializer(*args, **kwargs)


class ActivityViewSet(ActivityLogmessageLogger):
    serializer_class = serializers.ActivityDeserializer

    def get_serializer(self, *args, **kwargs) -> BaseSerializer:
        """ Override the default get_serializer to set editor_creation=True. """
        kwargs['editor_creation'] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if 'organisation_pk' in self.request.GET:
            return aims.Activity.objects.editables().filter(reporting_organisation_id=self.request.GET['organisation_pk'])
        return aims.Activity.objects.editables().all()


class Endorsement(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def user_can(self, action, activity_id, org_id=None, user=None):
        # where action is an HTTP verb
        if user is None:
            user = self.request.user
        # admins and anyone with the right perms can do anything
        if user_is_admin_or_superuser(user):
            return True

        user_org_ids = set()
        try:
            user_org_ids = set(user.userorganisation.organisations.values_list('code', flat=True))
        except AttributeError:
            # user is not part of any org, early exit
            return False

        def can_create_or_delete():
            if org_id is None:
                return False
            # allow only creation/deletion of endorsements in the name of any of the user's accountable orgs for this activity
            return all((
                # user is acting on behalf of one of its orgs
                org_id in user_org_ids,
                # and that org is an accountable for this activity
                aims.ActivityParticipatingOrganisation.objects.filter(activity_id=activity_id, role_id='Accountable', organisation_id=org_id).exists()
            ))

        verb_permission_map = dict(
            PUT=can_create_or_delete,  # noqa E2
            DELETE=can_create_or_delete,  # noqa E2
            )  # noqa E123

        return verb_permission_map[action.upper()]()

    def put(self, request, *args, **kwargs):
        act = kwargs['activity_pk']
        org = kwargs.get('org_pk')

        if not org:
            return HttpResponseBadRequest('No organisation ID specified')

        if not self.user_can('put', act, org_id=org):
            return Response('', status=status.HTTP_403_FORBIDDEN)

        created = False
        with transaction.atomic():
            endorsement, created = aims.ActivityEndorsement.objects.get_or_create(activity_id=act, organisation_id=org)
            if created:
                aims.ActivityLogmessage.objects.create(activity_id=act, body={'type': 'endorsement', 'action': 'add', 'uid': self.request.user.id, 'org_id': org})
        thestatus = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response('', status=thestatus)

    def delete(self, request, *args, **kwargs):
        act = kwargs['activity_pk']
        org = kwargs.get('org_pk')

        if not org:
            return HttpResponseBadRequest('No organisation ID specified')

        if not self.user_can('delete', act, org_id=org):
            return Response('', status=status.HTTP_403_FORBIDDEN)

        deleted = False
        with transaction.atomic():
            num_deleted, _ = aims.ActivityEndorsement.objects.filter(activity_id=act, organisation_id=org).delete()
            if num_deleted > 0:
                deleted = True
                aims.ActivityLogmessage.objects.create(activity_id=act, body={'type': 'endorsement', 'action': 'del', 'uid': self.request.user.id, 'org_id': org})
        if not deleted:
            return Http404
        return Response('', status=status.HTTP_204_NO_CONTENT)


class ActivityBudgetsViewSet(ActivityLogmessageLogger):
    serializer_class = serializers.ActivityBudgetDeserializer


class ActivityCompletionViewSet(ReadOnlyModelViewSet):
    queryset = aims.Activity.objects.all()
    serializer_class = serializers.ActivityCompletionSerializer


class ActivityResultsViewSet(ActivityLogmessageLogger):
    # TODO: Deprecated - remove once compatible with phd, hamutuk
    serializer_class = serializers.ActivityResultsDeserializer


class ActivityContactsViewSet(ActivityLogmessageLogger):
    serializer_class = serializers.ActivityContactSerializer


class ActivityTransactionsViewSet(ActivityLogmessageLogger):
    serializer_class = serializers.ActivityTransactionSerializer


class FormdataCreateModelMixin(mixins.CreateModelMixin):
    """
    Create a model instance. Data may optionally be wrapped in the request as '_data'.
    """

    def get_data(request):
        if '_data' in request.data:
            return request.data['_data']
        else:
            return request.data


class DocumentsViewset(AlwaysListViewSet):
    queryset = aims.DocumentLink.objects.all().prefetch_related('activity__title_set')
    serializer_class = serializers.DocumentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, ActivityPermission)

    def _guard_private_resources(self, qs):
        '''
        Restrict "private" documents to users
        Based on having "?private=true" as part of request string
        and being a super OR "?organisation=xxx" where
        the user making request is part of that organisation.
        Returns as suitably filtered Queryset based on these rules:
        1) No private documents by default
        2) No private documents to anonymous
        3) Regular users see their organisation's private docs when '?private=True'
        4) SU sees all docs when '?private=True'
        '''
        params = self.request.query_params
        user = self.request.user

        # The request must specifically ask for private resources
        # They are not returned by default
        private = params.get('private', False) == 'true'

        # Anonymous users always exclude private resources
        if user.is_anonymous:
            private = False

        # When "private" is not included in the query or user is anonymous
        # exclude all private documents
        # Note that this does not apply to POST, PATCH as DRF will otherwise
        # raise an error after creating a resource. DRF will prevent POST and PATCH
        # by unauthed user so this should not be a security risk.
        if self.request._request.method != 'GET':
            return qs

        if not private:
            return qs.exclude(private=True)

        # A regular User is prevented from seeing Private resources of organisations
        # which they are NOT affiliated with
        elif not user.is_anonymous and not user.is_staff:
            return qs.exclude(Q(organisation__in=user.userorganisation.organisations.all(), private=True))

        # When a staff user requests private documents
        # they may see all private documents from all organisations.
        # There are no restrictions.
        elif user.is_staff:
            return qs

    def get_queryset(self):
        '''
        Construct filters based on Activity or Organisation
        '''
        qs = super().get_queryset()
        params = self.request.query_params
        if 'activity' in params:
            qs = qs.filter(activity_id=params['activity'])
        if 'organisation' in params:
            qs = qs.filter(organisation_id=params['organisation'])

        qs = self._guard_private_resources(qs)

        return qs.order_by('-iso_date')

    def serialize_list_wrapper(self, response, status_code=None):
        """
        On a successful upload return all docs associated with this activity
        """
        queryset = self.get_queryset()
        serializer_class = serializers.DocumentSerializer
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status_code or response.status_code)

    def _set_categories(self, serializer, instance):
        category_keys = serializer.initial_data.get('categories', [])
        instance.categories.set(aims.DocumentCategory.objects.filter(pk__in=category_keys))

    def _set_file(self, serializer, instance):

        if '_file' in serializer.context['request'].FILES:
            if 'url' not in serializer.validated_data:
                serializer.validated_data['url'] = '<temp>'
            uploaded_file = serializer.context['request'].FILES['_file']
            upload = aims.DocumentUpload.objects.get_or_create(documentlink=instance)[0]
            upload.user = self.request.user
            upload.doc = uploaded_file
            upload.save()
            instance.url = upload.doc.url
            instance.file_format = aims.FileFormat.objects.get(code=uploaded_file.content_type)
            instance.save()

    def _set_narratives(self, serializer, instance):
        '''
        Create, update, remove operations for document narrative fields
        '''
        if 'narrative' not in serializer.initial_data:
            return
        model = instance.narrative.model
        narratives = serializer.initial_data['narrative']
        for narrative in narratives:
            description = narrative.get('description')
            language = narrative.get('language', 'en')

            if description is None or description == '':
                #  Delete narrative object where it is empty
                model.objects.filter(language=language, document=instance).delete()
            else:
                narrative_instance, _ = model.objects.get_or_create(
                    language_id=language,
                    document=instance)
                if narrative_instance.description != description:
                    narrative_instance.description = description
                    narrative_instance.save()

    def create(self, *args, **kwargs):
        try:
            aims.ActivityLogmessage.from_editor_request(
                self.request, activity=self.request.query_params["activity"]
            )
        except KeyError:
            # Hamutuk allows creating a Document without an Activity ID,
            # and this causes failure on save
            pass
        return super().create(*args, **kwargs)

    def update(self, *args, **kwargs):
        if self.get_object().activity_id:
            aims.ActivityLogmessage.from_editor_request(
                self.request, activity=self.get_object().activity_id
            )
        return super().update(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        aims.ActivityLogmessage.from_editor_request(
            self.request, activity=self.get_object().activity_id
        )
        return super().destroy(*args, **kwargs)

    def perform_create(self, serializer):
        self._user_has_permission(serializer)
        instance = serializer.save()
        self._set_file(serializer, instance)
        self._set_categories(serializer, instance)
        self._set_narratives(serializer, instance)

    def perform_update(self, serializer):
        self._user_has_permission(serializer)
        instance = serializer.save()
        self._set_file(serializer, instance)
        self._set_categories(serializer, instance)
        self._set_narratives(serializer, instance)

    def _user_membership(self):
        '''
        Return the Organisations and Reported Activities
        associated with this request
        '''
        user = self.request.user
        orgs = aims.Organisation.objects.filter(users__user=user)
        acts = aims.Activity.objects.editables().filter(reporting_organisation__users__user=user)
        return orgs, acts

    def perform_destroy(self, instance):
        self._user_has_delete_permission(instance)
        super().perform_destroy(instance)

    def _user_has_delete_permission(self, instance):
        """
        Similar to the _user_has_permission but here we're dealing with an instance
        rather than a serializer
        """
        organisations, activities = self._user_membership()
        valid_org = (instance.organisation in organisations) or instance.organisation is None
        valid_act = (instance.activity in activities) or instance.activity is None

        # Return if we have a valid org, act
        if (valid_org and valid_act) or (self.request.user.is_staff):
            return

        # Raise a ValidationError if user making request is not a part of this org/activity
        raise ValidationError(detail="User organisation or reported activities don't match request data")

    def _user_has_permission(self, serializer):
        """
        Assert that the User making a create / update request is permitted to do so
        """

        # List the valid Organisation and Activity (allowing None and empty string)
        organisations, activities = self._user_membership()
        organisation_pks = list(organisations.values_list('pk', flat=True))
        organisation_pks.extend([None, ''])
        activity_pks = list(activities.values_list('pk', flat=True))
        activity_pks.extend([None, ''])

        # Get the "initial" data passed to the serializer and run a validity check
        initial = serializer.initial_data
        valid_org = initial.get('organisation', None) in organisation_pks
        valid_act = initial.get('activity', None) in activity_pks

        # Return if we have a valid org, act, or an elevated user
        if (valid_org and valid_act) or (self.request.user.is_superuser or self.request.user.is_staff):
            return

        # Raise a ValidationError if user making request is not a part of this org/activity
        raise ValidationError(detail="User organisation or reported activities don't match request data")


def session_params(request):

    if request.method == 'GET':
        return JsonResponse(request.session._session)

    if request.method == 'POST':
        for k, v in request.POST.items():
            if k == 'csrfmiddlewaretoken':
                continue
            else:
                request.session[k] = v
        return JsonResponse(request.session._session)
