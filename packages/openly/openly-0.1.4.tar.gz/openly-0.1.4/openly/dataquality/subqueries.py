import logging
from datetime import datetime
from typing import Any, Dict, List, Tuple

from django.db.models import (
    Count,
    Exists,
    IntegerField,
    OuterRef,
    Q,
    QuerySet,
    Subquery,
    Sum,
)

from aims import models as aims
from profiles_v2.models import Person

logger = logging.getLogger(__name__)


def transaction_properties(
    attrs: List = [
        "aid_type",
        "finance_type",
        "value_date",
        "transaction_date",
        "provider_organisation",
        "receiver_organisation",
    ],
    outer_ref_fields: Tuple[str, str] = ("activity_id", "id"),
) -> Dict[str, Exists]:
    """
    Return a dict where the key is the annotated field and the value is
    an Exists for null attributes
    :param attr: List of attributes to return a "is null" check for
    :param outerref: A tuple of attributes to use for a Subquery "OuterRef".

    By default the outerref connects the transaction's "activity_id" with an "id" field.
    To make this suitable for finding Transactions matching these criteria you might use('id', 'id').
    """

    def activity_transaction_property(
        filt: Dict = None, excludes: Dict = None
    ) -> Exists:
        """
        Return an 'Exists' where activity transactions match certain criteria
        """
        transactions = aims.Transaction.objects.all()
        if filt:
            transactions = transactions.filter(**filt)
        if excludes:
            transactions = transactions.filter(**excludes)
        outer_ref = {outer_ref_fields[0]: OuterRef(outer_ref_fields[1])}
        return Exists(transactions.filter(**outer_ref))

    key = "null_transaction_%s"
    null_check = "%s__isnull"

    queries = {}
    for null_attr in attrs:
        query_key = key % (
            null_attr,
        )  # This is the name of the annotation field addded to Activity QuerySet
        filt = {null_check % (null_attr,): True}  # Filtering criteria

        if null_attr == "receiver_organisation":
            #  Special handling for 'receiver' becase an Expenditure is allowed to have a null Receiver
            queries[query_key] = activity_transaction_property(
                filt, dict(transaction_type="E")
            )
            continue

        queries[query_key] = activity_transaction_property(filt)

    return queries


class DataQualityQuery:

    """
    Each of the methods here returns a Subquery and a "pass" value
    In type annotation terms, -> Tuple[Subquery, Any]
    """

    @staticmethod
    def dac_3() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.ActivitySector.objects.filter(
                    activity__openly_status="published",
                    sector__in=aims.IATISector.dac_3.all(),
                ).filter(activity_id=OuterRef("id"))
            ),
            False,
        )

    @staticmethod
    def dac_5_sector_sum() -> Tuple[Subquery, int]:
        return (
            Subquery(
                aims.Activity.objects.filter(
                    openly_status="published",
                    activitysector__sector__in=aims.IATISector.dac_5.all(),
                )
                .annotate(Sum("activitysector__percentage"))
                .filter(id=OuterRef("id"))
                .values("activitysector__percentage__sum"),
                output_field=IntegerField(),
            ),
            100,
        )

    @staticmethod
    def national_sector_sum() -> Tuple[Subquery, int]:
        return (
            Subquery(
                aims.Activity.objects.filter(
                    openly_status="published",
                    activitysector__sector__in=aims.NationalSector.objects.all(),
                )
                .annotate(Sum("activitysector__percentage"))
                .filter(id=OuterRef("id"))
                .values("activitysector__percentage__sum"),
                output_field=IntegerField(),
            ),
            100,
        )

    @staticmethod
    def sector_zero() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.ActivitySector.objects.filter(
                    sector__in=aims.IATISector.objects.all()
                )
                .filter(Q(percentage=0) | Q(percentage__isnull=True))
                .filter(activity_id=OuterRef("id"))
            ),
            False,
        )

    @staticmethod
    def national_sector_zero() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.ActivitySector.objects.filter(
                    sector__in=aims.NationalSector.objects.all()
                )
                .filter(Q(percentage=0) | Q(percentage__isnull=True))
                .filter(activity_id=OuterRef("id"))
            ),
            False,
        )

    @staticmethod
    def sector_exists() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.ActivitySector.objects.filter(
                    sector__in=aims.IATISector.objects.all()
                ).filter(activity_id=OuterRef("id"))
            ),
            True,
        )

    @staticmethod
    def coordination_body_exists() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.ActivitySector.objects.filter(
                    sector__in=aims.NationalSector.objects.all()
                ).filter(activity_id=OuterRef("id"))
            ),
            True,
        )

    @staticmethod
    def location_sum() -> Tuple[Subquery, int]:
        return (
            Subquery(
                aims.Activity.objects.filter(openly_status="published")
                .annotate(Sum("location__percentage"))
                .filter(id=OuterRef("id"))
                .values("location__percentage__sum"),
                output_field=IntegerField(),
            ),
            100,
        )

    @staticmethod
    def no_locations() -> Tuple[Exists, bool]:
        return Exists(aims.Location.objects.filter(activity_id=OuterRef("id"))), True

    @staticmethod
    def location_with_zero_or_null() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.Location.objects.filter(
                    Q(percentage=0) | Q(percentage__isnull=True)
                ).filter(activity_id=OuterRef("id"))
            ),
            False,
        )

    @staticmethod
    def locations_multiple_levels() -> Tuple[Subquery, int]:
        return (
            Subquery(
                aims.Activity.objects.annotate(
                    Count("location__area__kind", distinct=True)
                )
                .values("location__area__kind__count")
                .filter(id=OuterRef("id"))
            ),
            1,
        )

    @staticmethod
    def past_planned_end_date() -> Tuple[Exists, bool]:
        return (
            Exists(
                aims.Activity.objects.filter(
                    openly_status="published",
                    activity_status=2,
                    end_planned__lte=datetime.today(),
                    id=OuterRef("id"),
                )
            ),
            False,
        )

    @staticmethod
    def implementation_end_date() -> Tuple[Subquery, bool]:
        return (
            Exists(
                aims.Activity.objects.filter(
                    activity_status__name="Implementation",
                    end_actual__isnull=False,
                    id=OuterRef("id"),
                )
            ),
            False,
        )


def activity_properties(
    attrs=["dac_3", "dac_5_sector_sum"], anno_param: str = "dq_%s"
) -> Tuple[Dict[str, Subquery], Dict[str, Any]]:
    """
    Returns a dict where the key is the annotated field and the value
    is an Exists or a Subquery for an Activity dataquality check

    This is useful for annotating multiple DataQualityChecks onto a QuerySet
    e.g. show all failing Activities for an Organisation
    """
    queries = {}
    expected_values = {}

    #  Prefix annotation with our 'annotation' parameter
    for attr in attrs:
        query_key = anno_param % (attr,)
        #  String lookup on the DQQ class - Expects a function which returns () -> Tuple[Subquery, Any]
        get_function = getattr(DataQualityQuery, attr)
        data_quality_subquery, expected_value = get_function()
        queries[query_key] = data_quality_subquery
        expected_values[query_key] = expected_value

    return queries, expected_values


def activity_quality_queryset(query: str = "dac_3") -> QuerySet:
    """
    Returns a queryset of failing activities from a DataQuality check
    This is useful for showing a list of objects which need attention
    Pulls one test from the `DataQualityQuery` set
    """
    q, v = activity_properties([query])
    logger.info(q)
    logger.info(v)
    return aims.Activity.objects.annotate(**q).exclude(**v)


def activity_transaction_quality_queryset(query: str) -> QuerySet:
    """
    Returns a Queryset of activities where one or more Transactions fails a
    dataquality check. Pulls one test from the `transaction_properties` function
    """
    q = transaction_properties([query], outer_ref_fields=("activity_id", "id"))  # :Dict
    annotation_name = list(q.keys())[0]
    queryset = aims.Activity.objects.annotate(**q).exclude(**{annotation_name: False})
    return queryset


def transaction_quality_queryset(query: str) -> QuerySet:
    """
    Returns a QuerySet of Transactions which fail a give quality check.
    Pulls one test from the `transaction_properties` function, adjusted to suit Transactions
    rather than the default return of a SubQuery to annotate Activity
    """
    q = transaction_properties([query], outer_ref_fields=("id", "id"))  # :Dict
    annotation_name = list(q.keys())[0]
    queryset = aims.Transaction.objects.annotate(**q).exclude(
        **{annotation_name: False}
    )
    return queryset


def org_name_null() -> QuerySet:
    """
    Return Organisations without a name
    """
    return aims.Organisation.objects.filter(Q(name="") | Q(name__isnull=True))


def person_name_null() -> QuerySet:
    """
    Return Persons without a name
    """
    return Person.objects.filter(Q(name="") | Q(name__isnull=True))
