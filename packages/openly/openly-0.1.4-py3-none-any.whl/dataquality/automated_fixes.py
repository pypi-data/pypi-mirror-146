import logging

from django.conf import settings
from django.db.models import Count, F, Sum
from django.db.models.functions import Coalesce

from aims.models import Activity, ActivitySector, Transaction

fix_enabled = getattr(settings, "ENABLE_AUTOFIX", False)

logger = logging.getLogger(__name__)


def activity_set_default_aid_type():
    """
    Return activities for which we do NOT have a default aid type, but ALL transactions on this activity
    share an aid type which we might use as the default
    """
    logger.info("activity_set_default_aid_type")

    sql = """
        SELECT
          a.id,
          (ARRAY_AGG(DISTINCT t.aid_type_id))[1] transaction_aid_type
          -- Select the aid type used by ALL transactions on this activity
        FROM
          aims_transaction t
          LEFT JOIN aims_activity a ON t.activity_id = a.id
        WHERE a.default_aid_type_id IS NULL
        GROUP BY a.id
        HAVING COUNT(DISTINCT t.aid_type_id) > 0 -- Don't include "null" as an aid type
    """
    for activity in Activity.objects.raw(sql):
        logger.info("Setting %s to %s", activity.id, activity.transaction_aid_type)
        activity.default_aid_type_id = activity.transaction_aid_type
        if fix_enabled:
            activity.save()


def activity_set_default_finance_type():
    """
    Return activities for which we do NOT have a default finance type, but ALL transactions on this activity
    share an finance type which we might use as the default
    """
    logger.info("activity_set_default_finance_type")
    sql = """
        SELECT
          a.id,
          (ARRAY_AGG(DISTINCT t.finance_type_id))[1] transaction_finance_type
          -- Select the finance type used by ALL transactions on this activity
        FROM
          aims_transaction t
          LEFT JOIN aims_activity a ON t.activity_id = a.id
        WHERE a.default_finance_type_id IS NULL
        GROUP BY a.id
        -- Don't include "null" as an finance type
        HAVING COUNT(DISTINCT t.finance_type_id) > 0
        """

    for activity in Activity.objects.raw(sql):
        logger.info("Setting %s to %s", activity.id, activity.transaction_finance_type)
        activity.default_finance_type_id = activity.transaction_finance_type
        if fix_enabled:
            activity.save()


def transaction_set_finance_type():
    """
    Replace missing transaction finance types with the activity default
    """
    logger.info("Setting Transaction Finance Types")
    for transaction in (
        Transaction.objects.filter(
            activity__default_finance_type__isnull=False, finance_type__isnull=True
        )
        .prefetch_related("activity__default_finance_type")
        .all()
    ):
        logger.info(
            "Finance type of %s to %s",
            transaction.id,
            transaction.activity.default_finance_type,
        )
        transaction.finance_type = transaction.activity.default_finance_type
        if fix_enabled:
            transaction.save()


def transaction_set_aid_type():
    """
    Replace missing transaction aid types with the activity default
    """

    for transaction in (
        Transaction.objects.filter(
            activity__default_aid_type__isnull=False, aid_type__isnull=True
        )
        .prefetch_related("activity__default_aid_type")
        .all()
    ):
        logger.info(
            "Aid type of %s to %s",
            transaction.id,
            transaction.activity.default_aid_type,
        )
        transaction.aid_type = transaction.activity.default_aid_type
        if fix_enabled:
            transaction.save()


def transaction_set_provider_organization_activity_funder():
    """
    all transactions have a provider_organisation_id
    for incoming funds - if only one funding organisation => use funding organisation
    """
    qs = Transaction.objects.filter(
        # Select only where the provider is not set already
        provider_organisation_id__isnull=True,
        transaction_type_id="IF",  # and the transaction is 'INCOMING FUNDS'
    )
    # Filter to where there is only one Funding organisation present
    # for this activity
    qs = qs.filter(activity__participating_organisations__role="Funding")
    qs = qs.annotate(candidates=Count("activity__participating_organisations__role"))
    qs = qs.filter(candidates=1)
    qs = qs.annotate(
        organisation=F("activity__participating_organisations__organisation")
    )

    for transaction in qs:
        logger.info(
            "provider_organisation_id of %s to %s",
            transaction.id,
            transaction.organisation,
        )
        transaction.provider_organisation_id = transaction.organisation
        if fix_enabled:
            transaction.save()


def transaction_set_provider_organization_activity_provider():
    """
    all transactions have a provider_organisation_id
    for commitments, disbursement, expenditure - if only one funding organisation => use reporting organisation
    """
    qs = Transaction.objects.all()

    # Select only where the provider is not set already
    # and the transaction is in C, D or E type
    # Commitment, Disbursement, Expenditure
    qs = qs.filter(
        provider_organisation_id__isnull=True, transaction_type_id__in=["C", "D", "E"]
    )
    # Filter to where there is only one Funding organisation present
    # for this activity
    qs = qs.filter(activity__participating_organisations__role="Funding")
    qs = qs.annotate(candidates=Count("activity__participating_organisations__role"))
    qs = qs.filter(candidates=1)
    qs = qs.annotate(organisation=F("activity__reporting_organisation"))

    for transaction in qs:
        logger.info(
            "provider_organisation_id of %s to %s",
            transaction.id,
            transaction.organisation,
        )
        transaction.provider_organisation_id = transaction.organisation
        if fix_enabled:
            transaction.save()


def transaction_set_receiver_organisation_to_reporting_organisation():
    """
    all transactions have a receiver_organisation_id (830 missing) # (!!) for expenditure, we don’t expect this
    for incoming funds = > use reporting organisation
    """

    qs = Transaction.objects.filter(
        receiver_organisation_id__isnull=True, transaction_type_id="IF"
    ).select_related("activity__reporting_organisation__name")
    for transaction in qs.all():

        logger.info(
            "receiver_organisation of %s to %s",
            transaction.id,
            transaction.activity.reporting_organisation,
        )
        transaction.receiver_organisation = transaction.activity.reporting_organisation
        if fix_enabled:
            transaction.save()


def transaction_set_receiver_organisation_to_implementing_organisation():
    """
    for expenditure = > None? Or Implementing organisation
    for all other transaction types, if only one implementing organisation = > use implementing organisation
    """
    qs = Transaction.objects.all()
    qs = qs.filter(
        receiver_organisation_id__isnull=True, transaction_type_id__in=["C", "D"]
    )

    qs = qs.filter(activity__participating_organisations__role="Implementing")
    qs = qs.annotate(candidates=Count("activity__participating_organisations__role"))
    qs = qs.filter(candidates=1)
    qs = qs.annotate(
        organisation=F("activity__participating_organisations__organisation")
    )

    for transaction in qs.all():

        logger.info(
            "receiver_organisation of %s to %s",
            transaction.id,
            transaction.organisation,
        )
        transaction.receiver_organisation_id = transaction.organisation
        if fix_enabled:
            transaction.save()


def sole_activitysector_set_to_one_hundred():
    # The only sector on an activity, and the value is 0 or Null
    qs = (
        ActivitySector.objects.exclude(vocabulary_id="RO")
        .annotate(p=Coalesce(F("percentage"), 0), c=Count("activity__activitysector"))
        .filter(p=0, c=1)
        .select_related("sector__name")
    )

    for activitysector in qs:
        logger.info(
            "Sector -> 100: %s %s",
            activitysector.activity_id,
            activitysector.sector.name_en,
        )
        activitysector.percentage = 100
        if fix_enabled:
            activitysector.save()


def activity_sector_is_zero_and_sectors_already_on_activity():
    """
    where multiple sectors, with one sector > 0% => delete any sectors with 0%
    """
    qs = (
        ActivitySector.objects.exclude(vocabulary_id="RO")
        .annotate(p=Coalesce(F("percentage"), 0), c=Count("activity__activitysector"))
        .annotate(s=Sum("activity__activitysector__percentage"))
        .filter(p=0, c__gt=1, s__gt=0)
        .select_related("sector__name")
    )

    for activitysector in qs:
        logger.info(
            "Remove zero sector: %s %s",
            activitysector.activity_id,
            activitysector.sector.name_en,
        )
    if fix_enabled:
        qs.delete()


def activitysector_dac3_remove_id_also_has_nested_dac5():
    qs = ActivitySector.objects.raw(
        """
            SELECT dac3.id, dac3.activity_id act, dac3.sector_id sec
            FROM aims_activitysector dac5, aims_activitysector dac3
            WHERE dac5.activity_id = dac3.activity_id
            AND dac5.vocabulary_id = 'DAC-5'
            AND dac3.vocabulary_id = 'DAC-3'
            AND dac5.sector_id / 100 = dac3.sector_id
            AND dac3.percentage = dac5.percentage
        """
    )
    for activitysector in qs:
        logger.info(
            "Remove DAC3 sector with matched DAC5: %s %s",
            activitysector.act,
            "activitysector.sec",
        )
    if fix_enabled:
        #  qs.delete() # Does not work since this is a RawQuerySet
        [activitysector.delete() for activitysector in qs]


def activitysector_dac3_remove_if_sum_dac5_equals_dac3():
    qs = ActivitySector.objects.raw(
        """
            WITH d5 AS (
            SELECT
              id,
              percentage,
              activity_id,
              sector_id / 100 AS sector_category,
              SUM(percentage) OVER (partition by activity_id, sector_id / 100 ) AS total_dac3
            FROM aims_activitysector
            WHERE vocabulary_id = 'DAC-5'
        ),
          d3 AS (
            SELECT
              percentage,
              activity_id,
              sector_id,
              SUM(percentage) OVER (partition by activity_id)
            FROM aims_activitysector
            WHERE vocabulary_id = 'DAC-3'
        )
        SELECT
         d5.id,
         d3.percentage AS category_percentage,
         d5.sector_category,
         d3.percentage/total_dac3 * d5.percentage AS percentage_change,
         d5.percentage + d3.percentage/total_dac3 * d5.percentage AS new_percentage
        FROM d3, d5 WHERE d3.activity_id = d5.activity_id AND d5.sector_category = d3.sector_id;
    """
    )

    qs_dac3_to_drop = ActivitySector.objects.raw(
        """
      WITH d5 AS (SELECT activity_id, sector_id / 100 AS sector_category FROM aims_activitysector WHERE vocabulary_id = 'DAC-5'),
          d3 AS (SELECT id, activity_id, sector_id FROM aims_activitysector WHERE vocabulary_id = 'DAC-3')
        SELECT d3.id FROM d5 LEFT JOIN d3 ON d3.activity_id = d5.activity_id AND d5.sector_category = d3.sector_id WHERE d3.id IS NOT NULL;
        """
    )

    for activitysector in qs:
        logger.info(
            "%s DAC3 (%03.2f%% / %s%% ) -> DAC5(s):  %s -> %s (%03.2f%% -> %03.2f%%)",
            activitysector.activity_id,
            activitysector.percentage_change,
            activitysector.category_percentage,
            activitysector.sector_category,
            activitysector.sector_id,
            activitysector.percentage,
            activitysector.new_percentage,
        )
        if fix_enabled:
            activitysector.percentage = activitysector.new_percentage
            activitysector.save()

    for activitysector in qs_dac3_to_drop:
        try:
            logger.info(
                "Delete DAC3 amount due to matched DAC5(s): %s %s",
                activitysector.activity_id,
                activitysector.sector_id,
            )
            if fix_enabled:
                activitysector.delete()
        except ActivitySector.DoesNotExist:
            logger.warning("ActivitySector does not exist. Continuing")


def activitysector_rescale():
    """
    When the sum of sectors on an activity do not equal 100, make them equal 100
    """

    sql = """
        WITH q AS (
                SELECT
                  *,
                  round(percentage * (100 / sum), 2) AS recalculated
                FROM (
                       SELECT
                         activity_id,
                         id,
                         percentage,
                         SUM(percentage)
                         OVER (
                           PARTITION BY activity_id ) sum
                       FROM aims_activitysector
                       WHERE vocabulary_id != 'RO'
                     ) s
            ), d AS (
                  SELECT
                    activity_id,
                    id,
                    percentage,
                    recalculated,
                    SUM(recalculated)
                    OVER (
                      PARTITION BY activity_id ) AS sum_recalculated
                  FROM q
              WHERE sum != 100
            ), ranked AS (
              SELECT
                rank()
                OVER (
                  PARTITION BY activity_id
                  ORDER BY id ) rank,
                *
              FROM d
            ), final AS (
              SELECT
                id,
                recalculated + (100 - sum_recalculated) recalculated
              FROM ranked
              WHERE rank = 1 AND sum_recalculated != 100
              UNION SELECT
                      id,
                      recalculated
                    FROM ranked
                    WHERE sum_recalculated = 100 OR rank != 1
            ),
      annotated AS (
          SELECT final.id, title, percentage, recalculated,  aims_sector.name
          FROM final
            LEFT JOIN aims_activitysector ON final.id = aims_activitysector.id
            LEFT JOIN aims_activity ON aims_activitysector.activity_id = aims_activity.id
            LEFT JOIN aims_title ON aims_title.activity_id = aims_activity.id
            LEFT JOIN aims_sector ON aims_activitysector.sector_id = aims_sector.code
      )
    SELECT * from annotated
    """
    qs = ActivitySector.objects.raw(sql)
    for asector in qs:
        logger.info(
            "Sector %s (@) %s : %s -> %s",
            asector.name,
            asector.title,
            asector.percentage,
            asector.recalculated,
        )
        if fix_enabled:
            asector.percentage = asector.recalculated
            asector.save()


def set_dac5_where_its_the_only_one():
    """
    Some DAC3 options have only a single DAC5. When that is true, convert the DAC3 to the DAC5.
    """
    from django.db import connection

    if fix_enabled:
        # "Actually I just ran this code in dbshell."
        with connection.cursor() as cursor:
            cursor.execute(
                """
                ALTER TABLE  aims_activitysector ADD COLUMN new_sector_id int;
                WITH cats AS (SELECT aims_sector.code AS sector_id, aims_sectorcategory.code AS category_code, COUNT(*) OVER(PARTITION BY aims_sectorcategory.code) catcount FROM aims_sector, aims_sectorcategory WHERE aims_sector.category_id = aims_sectorcategory.code
                AND aims_sector.code > 1000),
                  categories_with_one_to_one AS (
                      SELECT *
                      FROM cats
                      WHERE catcount = 1
                      )
                UPDATE aims_activitysector SET new_sector_id = (SELECT sector_id FROM categories_with_one_to_one where aims_activitysector.sector_id = categories_with_one_to_one.category_code)
                where aims_activitysector.sector_id IN (SELECT category_code FROM categories_with_one_to_one);
                -- SELECT * FROM categories_with_one_to_one;
                UPDATE aims_activitysector SET vocabulary_id = 'DAC-5' WHERE new_sector_id IS NOT NULL;
                UPDATE aims_activitysector SET sector_id = new_sector_id WHERE new_sector_id IS NOT NULL;
                ALTER TABLE aims_activitysector DROP COLUMN new_sector_id;
                """
            )


def run_all():
    activity_set_default_aid_type()
    activity_set_default_finance_type()
    # Note the order here is important - run the Activity fixes first
    transaction_set_finance_type()
    transaction_set_aid_type()
    transaction_set_provider_organization_activity_funder()
    transaction_set_provider_organization_activity_provider()
    transaction_set_receiver_organisation_to_reporting_organisation()
    transaction_set_receiver_organisation_to_implementing_organisation()
    sole_activitysector_set_to_one_hundred()
    activity_sector_is_zero_and_sectors_already_on_activity()
    activitysector_dac3_remove_id_also_has_nested_dac5()
    activitysector_dac3_remove_if_sum_dac5_equals_dac3()
    activitysector_rescale()
    # set_dac5_where_its_the_only_one()


def count_dataquality_errors():
    # A way to measure what we're actually changing with our automated fixes
    return dict(
        default_aid_type__isnull=Activity.objects.filter(
            default_aid_type__isnull=True
        ).count(),
        default_finance_type__isnull=Activity.objects.filter(
            default_finance_type__isnull=True
        ).count(),
        aid_type__isnull=Transaction.objects.filter(aid_type__isnull=True).count(),
        finance_type__isnull=Transaction.objects.filter(
            finance_type__isnull=True
        ).count(),
        provider_organisation__isnull=Transaction.objects.filter(
            provider_organisation__isnull=True
        ).count(),
        receiver_organisation__isnull=Transaction.objects.filter(
            receiver_organisation__isnull=True
        ).count(),
        activitysector__percentage=Activity.objects.exclude(
            activitysector__vocabulary_id="RO"
        )
        .annotate(Sum("activitysector__percentage"))
        .exclude(activitysector__percentage__sum=100)
        .count(),
        activitysector_scg__percentage=Activity.objects.filter(
            activitysector__vocabulary_id="RO"
        )
        .annotate(Sum("activitysector__percentage"))
        .exclude(activitysector__percentage__sum=100)
        .count(),
    )
