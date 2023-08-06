from haystack import indexes
from aims import models as aims
from django.db.models import OuterRef, Subquery
from django.db.models import F, Value as V
from django.db.models.functions import Coalesce
from django.contrib.postgres.aggregates import StringAgg
import logging
logger = logging.getLogger(__name__)


class PartnerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    rendered_nav = indexes.CharField(use_template=True, indexed=False)
    rendered_search = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return aims.Partner

    def index_queryset(self, using=None):
        logger.debug('index_queryset called for PartnerIndex from %s', using)
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all().distinct()

    def update_object(self, instance, using=None, **kwargs):
        annotated_instance = self.index_queryset().get(pk=instance.pk)
        super().update_object(annotated_instance, using=None, **kwargs)


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    rendered_nav = indexes.CharField(use_template=True, indexed=False)
    rendered_search = indexes.CharField(use_template=True, indexed=False)
    openly_status = indexes.CharField(model_attr='openly_status')
    reporting_organisation_id = indexes.CharField(model_attr='reporting_organisation_id_or_empty')

    def get_model(self):
        return aims.Activity

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        logger.debug('index_queryset called for ActivityIndex from %s', using)
        qs = self.get_model().objects.all_openly_statuses()\
            .filter(openly_status__in=['published', 'draft'])
        with_ref = qs.filter(pk=OuterRef('pk'))

        # Subquery-Annotate 'annosectors'
        anno_sectors = with_ref.filter(activitysector__sector__category__openly_type='iati')\
            .annotate(anno=StringAgg('activitysector__sector__name', delimiter=', ')).values('anno')

        # Subquery-Annotate 'anno_descriptions'
        anno_descriptions = (
            aims.Description.objects.exclude(description='').  # Exclude all blank descriptions
            values('activity').  # This first 'values' is required for the StringAgg
            annotate(descriptions=StringAgg('description', '\n')).  # Join them with a newline
            filter(activity=OuterRef('pk')).  # This makes our Queryset into a Subquery
            values('descriptions')  # This selects the column to append to the OuterRef (ie the Activity)
        )
        anno_title = with_ref.annotate(anno=StringAgg('title__title', delimiter=', ', distinct=True)).values('anno')
        anno_locations = with_ref.annotate(anno=StringAgg('location__name', delimiter=', ', distinct=True)).values('anno')

        return self.get_model().objects.all_openly_statuses()\
            .filter(openly_status__in=['published', 'draft'])\
            .annotate(
                subquery_descriptions=Subquery(anno_descriptions[:1]),
                subquery_sectors=Subquery(anno_sectors[:1]),
                subquery_titles=Subquery(anno_title[:1]),
                subquery_locations=Subquery(anno_locations[:1]),
                reporting_organisation_id_or_empty = Coalesce(F("reporting_organisation_id"), V(""))
        )

    def update_object(self, instance, using=None, **kwargs):
        annotated_instance = self.index_queryset().get(pk=instance.pk)
        return super().update_object(annotated_instance, using=None, **kwargs)


class OrganisationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return aims.Organisation

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def update_object(self, instance, using=None, **kwargs):
        annotated_instance = self.index_queryset().get(pk=instance.pk)
        return super().update_object(annotated_instance, using=None, **kwargs)
