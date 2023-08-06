from django.apps import apps
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.cache import cache
from django.db.models import F, OuterRef, Subquery, TextField, Value as V
from django.db.models.expressions import Case, When
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from aims import models as aims
from aims.utils import get_rounded_budget


class BaseActivitiesPageView(TemplateView):
    """
    List of all activities in a table, used in DIRD
    This is derived from the Projectbank activity list
    and drops the additional financial data bits from the queryset
    """
    template_name = "activity_list/activity_list.html"

    def get_serialized_activities(self):
        """ Return a list of serialized activities, retrieved from cache if present. """
        CACHE_KEY = 'activity-list-serialized-activities'
        cached_activities = cache.get(CACHE_KEY)
        if cached_activities:
            return cached_activities

        activities = aims.Activity.objects.all().order_by('pk')\
            .select_related('activity_status') \
            .prefetch_related('title_set')

        serialized_activities = [{
            'id': a.pk,
            'profile_url': a.profile_url,
            'title': a.title,
            'status': a.status,
            'total_budget_raw': a.total_budget if a.total_budget else 0,
            'total_budget_rounded': get_rounded_budget(a.total_budget),
        } for a in activities]

        cache.set(CACHE_KEY, serialized_activities, 60)
        return serialized_activities

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Activity List')

        context['activities'] = self.get_serialized_activities()

        context['lookups'] = {
            'statuses': list(aims.ActivityStatus.objects.all().distinct().order_by('order', 'code').values('code', 'name'))
        }

        return context


class ActivitiesPageView(TemplateView):
    """
    List of all activities in a table, used in Project Bank.
    """
    template_name = "activity_list/activity_list.html"

    def get_serialized_activities(self):
        """ Return a list of serialized activities, retrieved from cache if present. """
        CACHE_KEY = 'activity-list-serialized-activities'
        cached_activities = cache.get(CACHE_KEY)
        if cached_activities:
            return cached_activities

        annotations_implementing_government_agency = Subquery(
            aims.ActivityParticipatingOrganisation.objects.filter(
                role_id="Accountable", activity_id=OuterRef("pk")
            )
            .values("activity_id")
            .annotate(
                anno=ArrayAgg(
                    Case(
                        # Show the organisation name by itself if
                        # there is no parent org
                        When(
                            organisation__parent__isnull=True,
                            then=F("organisation__name"),
                        ),
                        # Otherwise show the parennt code
                        # in brackets
                        When(
                            organisation__parent__isnull=False,
                            then=Concat(
                                "organisation__name",
                                V(" ("),
                                "organisation__parent__code",
                                V(")"),
                            ),
                        ),
                    )
                )
            )
            .values("anno")[:1],
            output_field=TextField(),
        )

        # Note that this funding_sources anno will only work for PB
        activities = aims.Activity.objects.all().order_by('pk')\
            .select_related('activity_status') \
            .prefetch_related('title_set') \
            .annotate(funding_sources=ArrayAgg('activityfundingsource__funding_source')) \
            .annotate(iga=annotations_implementing_government_agency)

        serialized_activities = [{
            'id': a.pk,
            'profile_url': a.profile_url,
            'title': a.title,
            'government_agency': a.iga[0] if a.iga else '',
            'status': a.status,
            'total_budget_raw': a.total_budget if a.total_budget else 0,
            'total_budget_rounded': get_rounded_budget(a.total_budget),
            'funding_sources': a.funding_sources,
        } for a in activities]

        cache.set(CACHE_KEY, serialized_activities, 60)
        return serialized_activities

    def get_context_data(self, **kwargs):
        context = super(ActivitiesPageView, self).get_context_data(**kwargs)
        context['page_title'] = _('Project List')

        context['activities'] = self.get_serialized_activities()

        context['lookups'] = {
            'funding_sources': list(apps.get_model('pb_profile', 'FundingSource').objects.all().order_by('name').values('code', 'name')),
            'statuses': list(aims.ActivityStatus.objects.all().distinct().order_by('order', 'code').values('code', 'name'))
        }

        return context
