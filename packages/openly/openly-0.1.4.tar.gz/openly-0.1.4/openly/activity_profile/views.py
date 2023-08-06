from django.conf import settings
from sentry_sdk import capture_exception
from django.urls import reverse
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from django.views.generic import TemplateView
from django.db.models import Sum
import logging

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from dashboard import charts

from aims import models as aims
from aims import base_utils
from aims.aggregates import Aggregates
from aims.api_serializers import serializers

from .models import ActivityProfile
from aims.utils import render, date_to_financial_year, get_rounded_budget

logger = logging.getLogger(__name__)


def activity_finance_data(activity):

    context = {}

    funding_organisations = aims.Organisation.objects.filter(transaction_providing_organisation__activity=activity).distinct()
    participating_organisations = activity.participating_organisations.filter(role__code__in=['Extending', 'Implementing'])
    ministry_organisations = activity.participating_organisations.filter(role__code='Accountable')

    total_commitments = charts.total_commitments(activity.transaction_set)
    total_disbursements = charts.total_disbursements(activity.transaction_set)

    percent_disbursed = charts.percent_disbursed(total_commitments, total_disbursements)
    transactions_by_month_year = charts.transactions_by_month_year([activity])

    context['funding_organisations'] = funding_organisations
    context['participating_organisations'] = participating_organisations
    context['ministry_organisations'] = ministry_organisations

    # context['total_commitment'] = base_utils.prettify_compact(activity.total_commitment)
    context['total_commitment_usd'] = base_utils.prettify_compact(activity.total_commitment_usd)

    context['percent_disbursed'] = percent_disbursed
    context['transactions_by_month_year'] = render(transactions_by_month_year)
    context['transaction_queryset'] = activity.transaction_set.all()

    context['transactions_json'] = render([{
        'aid_type': '{aid_type__code} - {aid_type__name}'.format_map(trans),
        'finance_type': '{finance_type__code} - {finance_type__name}'.format_map(trans),
        'provider_organisation': '{provider_organisation__name}'.format_map(trans),
        'receiver_organisation': '{receiver_organisation__name}'.format_map(trans),
        'tied_status': '{tied_status__code} - {tied_status__name}'.format_map(trans),
        'transaction_date': '{transaction_date}'.format_map(trans),
        'transaction_type': '{transaction_type__code} - {transaction_type__name}'.format_map(trans),
        'currency_code': '{currency__code}'.format_map(trans),
        'value': '{value}'.format_map(trans)
    } for trans in context['transaction_queryset'].values(
        'aid_type__code', 'aid_type__name', 'finance_type__code', 'finance_type__name', 'provider_organisation__name', 'receiver_organisation__name',
        'tied_status__code', 'tied_status__name', 'transaction_date', 'transaction_type__code', 'transaction_type__name', 'currency__code', 'value',
    )])

    commitments = activity.transaction_set.filter(transaction_type='C')
    single_category = commitments.distinct('aid_type__category').count() == 1

    currency_sums = {currency: value_sum for currency, value_sum in commitments.values('currency').annotate(Sum('value')).values_list('currency', 'value__sum')}
    pretty_sums = {currency: base_utils.prettify_compact(value_sum) for currency, value_sum in currency_sums.items()}

    context['commitment_by_currency'] = render(currency_sums)
    context['pretty_commitment_by_currency'] = render(pretty_sums)
    context['aid_type_categories'] = Aggregates(commitments).category_percentage_by_activity_str().get(activity.id, '')
    context['aid_type_categories_header'] = 'Aid Type Category' if single_category else 'Aid Type Categories'

    # Set the distinct finance types for this Activity's transactions
    finance_types = context['transaction_queryset'].filter(finance_type__isnull=False).distinct('finance_type')
    context['finance_types_list'] = ', '.join(finance_types.values_list('finance_type__name', flat=True))
    return context


class ActivityProfileView(TemplateView):
    template_name = "activity_profile/activity_profile.html"

    def get_context_data(self, **kwargs):
        context = super(ActivityProfileView, self).get_context_data(**kwargs)

        activity = get_object_or_404(
            aims.Activity.objects, id=unquote(self.kwargs['activity_id'])
        )  # type: aims.Activity
        context['page_title'] = '{} Activity Profile'.format(activity.title)
        organisation = activity.reporting_organisation
        activity_profile, _ = ActivityProfile.objects.get_or_create(activity=activity)
        editor = base_utils.check_editor_privilege(self.request.user, organisation)

        # Using a single-object queryset instead of a single object
        # allows some very powerful prefetching
        qs = serializers.ActivityDeserializer.eager_id(activity.id)

        contacts = serializers.ContactSerializer(activity.contactinfo_set.all(), many=True).data

        # Strip out sensitive contacts information from the contacts on the Activity Profile
        if self.request.user.is_anonymous:
            if not getattr(settings, 'CONTACTS_SHOWS_EMAILS', False):
                for contact in contacts:
                    contact.pop('email')
            if not getattr(settings, 'CONTACTS_SHOWS_PHONE', False):
                for contact in contacts:
                    contact.pop('telephone')

        context['activity'] = activity
        context['activity_title'] = activity.title
        activity_object = serializers.ActivityDeserializer(qs, many=True).data[0]
        context['activity_profile'] = activity_profile
        context['organisation_profile'] = reverse('organisation_profile', args=[organisation.pk])
        context['editor'] = editor
        context['contacts'] = render(contacts)
        context['areas'] = render({a['id']: a for a in aims.Area.objects.values('id', 'name', 'kind', 'parent')})
        context['partners'] = render({partner.code: reverse(
            'organisation_profile', args=[partner.pk]) for partner in aims.Partner.objects.all()})
        context['project_name'] = getattr(settings, 'PROJECT_NAME', "")
        context['activity_tags'] = render(self.get_activity_tags(activity))

        if getattr(settings, 'ACTIVITY_PROFILE_DATES_FINANCIAL_YEAR', False):
            # transform actual start and end dates into the financial year format
            activity_object['activity_dates'][0]['type']['name'] = 'Start'
            activity_object['activity_dates'][0]['iso_date'] = date_to_financial_year(activity_object['activity_dates'][0]['iso_date'])
            activity_object['activity_dates'][2]['type']['name'] = 'End'
            activity_object['activity_dates'][2]['iso_date'] = date_to_financial_year(activity_object['activity_dates'][2]['iso_date'])

        # Include a modified form of the date which indicates date precision.
        date_choices = activity.ActivityDateTypeChoices

        # Add a "detail" and "display_date" field to each serialized date
        for date_object in activity_object['activity_dates']:
            detail = None
            display_date = None

            if not date_object['iso_date']:
                continue

            # Lookup the relevant enum for the date type from the serialized data
            date_type = date_choices(date_object['type']['code'])

            if date_type == date_choices.PLANNED_START:
                detail = activity.start_planned_detail
                display_date = activity.start_planned_display
            elif date_type == date_choices.PLANNED_END:
                detail = activity.end_planned_detail
                display_date = activity.end_planned_display
            elif date_type == date_choices.ACTUAL_START:
                detail = activity.start_actual_detail
                display_date = activity.start_actual_display
            elif date_type == date_choices.ACTUAL_END:
                detail = activity.end_actual_detail
                display_date = activity.end_actual_display
            date_object['detail'] = detail
            date_object['display_date'] = display_date

        if getattr(settings, 'ACTIVITY_PROFILE_SHOW_TOTAL_BUDGET', False):
            if 'dird_templates' in settings.INSTALLED_APPS:
                if hasattr(activity, 'activityfinances'):
                    activity_object['total_budget'] = get_rounded_budget(activity.activityfinances.estimated_budget, 'K')
                else:
                    activity_object['total_budget'] = 'K -'
            else:
                activity_object['total_budget'] = get_rounded_budget(activity.total_budget)

        context['activity_object'] = render(activity_object)

        if getattr(settings, 'EDITOR_SIMPLE_SECTORS', False):
            sectors = activity.activitysector_set.all().values('sector__code', 'sector__name').distinct()
        else:
            sectors = activity.activitysector_set.filter(vocabulary='DAC-5').values('sector__code', 'sector__name').distinct()
        sectors = [{'code': sector['sector__code'], 'name': sector['sector__name']} for sector in sectors]
        context['sectors'] = render(sectors)

        try:
            context['map_config'] = render(settings.LEAFLET_CONFIG)
        except Exception:
            context['map_config'] = render({})
        context['token'] = self.request.META.get('CSRF_COOKIE', None)
        documents = []
        for doc in activity.documentlink_set.order_by('-upload__modified'):
            try:
                # lookup category code for the doc
                doc_cats = doc.categories.all()
                if hasattr(doc, 'upload'):
                    try:
                        size = doc.upload.doc.size
                    except FileNotFoundError as exception:
                        if settings.DEBUG:
                            logger.warning('%s', exception)
                        else:
                            capture_exception(exception)
                        size = None
                    documents.append({
                        'title': doc.title,
                        'download_url': doc.upload.doc.url,
                        'last_modified': doc.upload.modified,
                        'size': size,
                        'file_type': doc.file_format.code,
                        'missing': size is None,
                        'category': doc_cats[0].name if len(doc_cats) > 0 else None
                    })
                else:
                    documents.append({
                        'title': doc.title,
                        'download_url': None if doc.url == '' else doc.url,
                        'last_modified': None,
                        'size': 0,
                        'file_type': None,
                        'missing': doc.url is None or doc.url == '',
                        'category': doc_cats[0].name if len(doc_cats) > 0 else None
                    })
            except Exception:  # pylint: disable=W0703
                if settings.DEBUG:
                    raise
                else:
                    capture_exception()
        context['documents'] = render(documents)
        context['financial_data_exists'] = getattr(settings, 'FINANCIAL_DATA_EXISTS', False)
        context['hide_map'] = getattr(settings, 'ACTIVITY_PROFILE_HIDE_MAP', False)

        if context['financial_data_exists']:
            context.update(activity_finance_data(activity))

        return context

    def get_activity_tags(self, activity):
        """ Get the ActivityTag objects for this activity in the format
        { tag_vocabulary_name: [tag_1_name, tag_2_name, ...] }
        ex: { "Sustainable Development Goals": ["5. Gender Equality", "10. Reducing Inequality", ...] }
        """
        tags = activity.tag.all().order_by('pk')
        if len(tags) == 0:
            return {}
        if len(set([t.vocabulary_id for t in tags])) > 1:
            logger.warn('Activity {} has tags with more than one vocabulary'.format(activity.pk))
        # for now, only display tags from the first vocabulary
        master_vocabulary = tags[0].vocabulary
        tags = [t for t in tags if t.vocabulary_id == master_vocabulary.pk]
        return {master_vocabulary.name: [{'name': t.name, 'code': t.code} for t in tags]}


class ActivityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = serializers.ActivityDeserializer
    queryset = aims.Activity.objects.all()
    # Public end point - expressly permit reading
    permission_classes = [IsAuthenticatedOrReadOnly]
