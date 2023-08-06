import logging
from collections import OrderedDict, defaultdict
from django.contrib.auth.models import AbstractUser

from django.db.models import Manager, QuerySet, Q
from django.db.models.base import ModelBase
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.apps import apps

from typing import Dict, Any, Mapping, Optional, Union, List  # noqa: F401

from export.views import ExportActivities, ExportTransactions, QueryFilter

from .serializers import ActivitySerializer
from .subqueries import (
    activity_quality_queryset as aqq,
    transaction_quality_queryset as tqq,
    org_name_null,
)

from aims.models import Organisation

logger = logging.getLogger(__name__)


def recursive_dd() -> 'defaultdict[Any, Any]':
    return defaultdict(recursive_dd)


class TestModel:

    #  Hash to determine how to filter if an 'org code' is specified
    filter_for_organisation = {
        "persons": "organisation_profile__organisation__code",
        "activity": "reporting_organisation_id",
        "activity_transactions": "reporting_organisation__code",
        "activityprofile": "reporting_organisation__code",
        "sectors_and_coordination_bodies": "activitysector__activity__reporting_organisation__code",
        "locations": "reporting_organisation__code",
        "activity_organisations": "reporting_organisation__code",
        "transaction": "activity__reporting_organisation__code",
        "organisationprofile": "organisation__code"
    }

    @classmethod
    def get_test(cls, category, title: str, user: AbstractUser):
        user_organisation = Organisation.objects.filter(users__user=user).first()
        org_code = user_organisation.code if user_organisation else None
        all_tests = test_models(org_code)
        try:
            category_tests = all_tests[category]
        except KeyError as exc:
            raise KeyError(
                "Category %s not in test groups. Try one of %s",
                category,
                all_tests.keys(),
            ) from exc
        try:
            return category_tests[title]
        except KeyError as exc:
            raise KeyError(
                "Test %s not in test groups %s. Try one of %s"
                % (title, category, category_tests.keys())
            ) from exc

    def __init__(self, nickname, title, model, category="activity", org=None, **kwargs):
        """
        :param nickname:
        :param title:
        :param model: Model instance or Manager instance
        :param category: Which group to place the test in - Template accesses this to provide URLs
        :param kwargs: Dict providing optional params "objects" (name of manager in model), "url_anchor"
        """

        always_prefetch = {"activity": ("title_set",)}
        self.org = org
        self.title = title
        self.id = id
        if callable(model):
            model = model()
        if (
            not isinstance(model, ModelBase)
            and not isinstance(model, Manager)
            and not isinstance(model, QuerySet)
        ):
            raise TypeError(
                "Expected a subclass of Model or Manager as an argument - received %s"
                % (type(model))
            )
        self.objects = (
            getattr(model, kwargs.pop("objects", "objects"))
            if isinstance(model, ModelBase)
            else model
        )
        self.nickname = nickname
        self.category = category
        self.url_anchor = kwargs.pop("url_anchor", None)

        if "select_related" in kwargs:
            self.objects = self.objects.select_related(*kwargs["select_related"])
        prefetch = list(kwargs.get("prefetch_related", []))
        prefetch.extend(always_prefetch.get("category", []))
        if prefetch:
            self.objects = self.objects.prefetch_related(*kwargs["prefetch_related"])

        if self.org and self.objects:
            if self.category not in self.filter_for_organisation:
                raise AssertionError(
                    'Asked to filter by organisation but this category of TestModel "%s" does not know how to, please amend TestModel.filter_for_organisation'
                    % (self.category,)
                )
            self.objects = self.objects.filter(
                **{self.filter_for_organisation[self.category]: self.org}
            )

    @property
    def count(self):
        try:
            return self.objects.count()
        except Exception as E:
            logger.error(
                "Oops on dataquality test: %s %s %s",
                self.nickname,
                self.title,
                self.category,
            )
            raise AssertionError("Error getting Count") from E


def test_models(user_org: Optional[Organisation] = None) -> Mapping[str, TestModel]:
    """
    Add TestModel instances
    """

    tests = [
        # Transaction tests
        TestModel(
            "t_aid_type",
            "A transaction must have an aid type",
            tqq("aid_type"),
            "transaction",
            url_anchor="#finances/transactions",
            org=user_org,
        ),
        TestModel(
            "t_finance_type",
            "A transaction must have a finance type",
            tqq("finance_type"),
            "transaction",
            url_anchor="#finances/transactions",
            org=user_org,
        ),
        TestModel(
            "t_provider",
            "A transaction must have an providing organisation",
            tqq("provider_organisation"),
            "transaction",
            url_anchor="#finances/transactions",
            org=user_org,
        ),
        TestModel(
            "t_receiver",
            "A transaction (excluding expenditure) must have a receiving organisation",
            tqq("receiver_organisation"),
            "transaction",
            url_anchor="#finances/transactions",
            org=user_org,
        ),
        TestModel(
            "t_value_date",
            "A transaction must have a value date",
            tqq("value_date"),
            "transaction",
            url_anchor="#finances/transactions",
            org=user_org,
        ),
        TestModel(
            "t_transaction_date",
            "A transaction must have a transaction date",
            tqq("transaction_date"),
            "transaction",
            url_anchor="#finances/transactions",
            org=user_org,
        ),
        # There are 5 tests for sectors_and_coordination_bodies
        TestModel(
            "a_sector_total",
            "An activity's sectors must add up to one hundred percent",
            aqq("dac_5_sector_sum"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_sectorcg_total",
            "An activity's coordination bodies must add up to one hundred percent",
            aqq("national_sector_sum"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_dac3_sector",
            "An activity’s sectors must all come from the DAC5 sub-sector list",
            aqq("dac_3"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_no_sector_zero",
            "An activity’s sectors must never be zero percent",
            aqq("sector_zero"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_national_sector_zero",
            "An activity’s coordination bodies must never be zero percent",
            aqq("national_sector_zero"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_sector_zero_new",
            "An activity must have at least one sector",
            aqq("sector_exists"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_sector_zero_new",
            "An activity must have at least one coordination body",
            aqq("coordination_body_exists"),
            category="sectors_and_coordination_bodies",
            url_anchor="#sectors",
            org=user_org,
        ),
        TestModel(
            "a_location_total",
            "An activity's locations must add up to one hundred percent",
            aqq("location_sum"),
            category="locations",
            url_anchor="#locations",
            org=user_org,
        ),
        TestModel(
            "a_no_locations",
            "An activity must have at least one location",
            aqq("no_locations"),
            category="locations",
            url_anchor="#locations",
            org=user_org,
        ),
        TestModel(
            "a_mixed_locations",
            "An activity's locations must all be at the same administrative level",
            aqq("locations_multiple_levels").filter(dq_locations_multiple_levels__gt=0),
            category="locations",
            url_anchor="#locations",
            org=user_org,
        ),
        TestModel(
            "a_location_zero",
            "An activity's locations must never be zero percent",
            aqq("location_with_zero_or_null"),
            category="locations",
            url_anchor="#locations",
            org=user_org,
        ),
        TestModel(
            "a_past_planned",
            "An activity should not be under implementation and past the planned end date",
            aqq("past_planned_end_date"),
            url_anchor="#general",
            org=user_org,
        ),
        TestModel(
            "a_commitment",
            "An activity should have at least one Commitment transaction",
            apps.get_model("aims", "activity").objects.exclude(
                transaction__transaction_type="C"
            ),
            url_anchor="#finances/transactions",
            org=user_org,
            category="activity_transactions",
        ),
        TestModel(
            "a_implementing",
            "An activity must have an Implementing organisation",
            apps.get_model("aims", "activity").objects.exclude(
                participating_organisations__role="Implementing"
            ),
            url_anchor="#part_orgs",
            org=user_org,
            category="activity_organisations",
        ),
        # TestModel(
        #     "a_participating",
        #     "An activity should have at least one Accountable organisation",
        #     apps.get_model("aims", "activity").objects.exclude(
        #         participating_organisations__role="Accountable"
        #     ),
        #     url_anchor="#part_orgs",
        #     org=user_org,
        #     category="activity_organisations",
        # ),
        # TestModel(
        #     "a_extending",
        #     "An activity should have at least one Extending organisation",
        #     apps.get_model("aims", "activity").objects.exclude(
        #         participating_organisations__role="Extending"
        #     ),
        #     url_anchor="#part_orgs",
        #     org=user_org,
        #     category="activity_organisations",
        # ),
        TestModel(
            "a_implementation_endddate",
            'An activity with an "Implementation" status should not have an "Actual End Date" set',
            aqq("implementation_end_date"),
            url_anchor="#general",
            org=user_org,
        ),
        TestModel(
            "organisation_names",
            "An organisation title should never be blank",
            org_name_null,
            "organisations",
            org=user_org,
        ),
        TestModel(
            "activity_profile_image",
            "An activity should have a cover image",
            apps.get_model("aims", "activity").objects.filter(
                profile__banner_image=""
            ),
            "activityprofile",
            org=user_org,
        ),
        TestModel(
            "organisation_profile_image",
            "An organisation should have a logo",
            apps.get_model("profiles_v2", "OrganisationProfile").objects.filter(
                logo=""
            ),
            "organisationprofile",
            org=user_org,
        ),
        TestModel(
            "organisation_banner_image",
            "An organisation should have a banner",
            apps.get_model("profiles_v2", "OrganisationProfile").objects.filter(
                banner_image=""
            ),
            "organisationprofile",
            org=user_org,
        ),
        TestModel(
            "a_has_planned_startdate",
            "An activity must have a planned start date",
            apps.get_model("aims", "activity").objects.exclude(
                start_planned__isnull=False
            ),
            url_anchor="#general",
            org=user_org,
        ),
        TestModel(
            "a_has_planned_enddate",
            "An activity must have a planned end date",
            apps.get_model("aims", "activity").objects.exclude(
                end_planned__isnull=False
            ),
            url_anchor="#general",
            org=user_org,
        ),
        TestModel(
            "a_implemented_has_actualstart",
            "An activity being implemented must have an Actual Start Date",
            apps.get_model("aims", "activity")
            .objects.exclude(start_actual__isnull=False)
            .filter(activity_status__name="Implementation"),
            url_anchor="#general",
            org=user_org,
        ),
        TestModel(
            "a_implemented_has_actualstart",
            "An activity being completed must have an Actual End Date",
            apps.get_model("aims", "activity")
            .objects.exclude(end_actual__isnull=False)
            .filter(activity_status__name="Completion"),
            url_anchor="#general",
            org=user_org,
        ),
        # This one is disabled because it's a bit confusing for users
        # TestModel(
        #     'person_no_name',
        #     'A Person should not have an empty field for Name',
        #     person_name_null,
        #     'persons',
        #     org=user_org
        # )
    ]
    ordered_tests = OrderedDict()  # type: Dict[str, Any]

    # Generate profile fields missing data tests
    for (
        profile_field
    ) in "address,phone_number,email,website,facebook,twitter,fax".split(","):

        if profile_field in ["facebook", "twitter"]:
            test_title = "An organisation profile should have a {} profile link".format(profile_field)
        elif profile_field == 'address':
            test_title = "An organisation profile must have an office {}".format(profile_field)
        else:
            test_title = "An organisation profile must have an {}".format(profile_field.replace('_', ' '))

        objects = apps.get_model("profiles_v2", "organisationprofile").objects.filter(
            Q(**{"contact_info__%s__isnull" % (profile_field): True})
            | Q(**{"contact_info__%s" % (profile_field): ""})
        )

        tests.append(TestModel(
            "o_profile_has_{}".format(profile_field),
            test_title,
            objects,
            category="organisationprofile",
            org=user_org,
        ))

    for t in tests:
        if t.category not in ordered_tests:
            ordered_tests[t.category] = OrderedDict()
        ordered_tests[t.category][t.nickname] = t

    return ordered_tests


class QualityAssuranceIndex(TemplateView):
    template_name = "dataquality/aims_quality_assurance.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user_org = Organisation.objects.filter(users__user=self.request.user).first()  # type: Union[Organisation, None]

        c = {"tests": test_models(user_org)}
        return c


class QualityAssuranceTest(TemplateView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        cat = kwargs["category"]
        nick = kwargs["nickname"]

        user_org = Organisation.objects.filter(users__user=self.request.user).first()

        try:
            test = test_models(user_org)[cat][nick]
        except KeyError:
            raise KeyError("Invalid test name")

        # check to handle person results filtering
        if cat == "persons" and user_org:
            objects = test.objects.filter(
                organisation_profile__organisation__code=user_org.code
            ).all()  # type: QuerySet
        else:
            objects = test.objects.all()  # type: QuerySet

        return {
            "category": kwargs["category"],
            "nickname": kwargs["nickname"],
            "test": test,
            "objects": objects,
        }

    def get_template_names(self) -> List[str]:
        cat = self.kwargs["category"]
        if cat in [
            "activity",
            "activity_organisations",
            "activity_transactions",
            "sectors_and_coordination_bodies",
            "locations",
            "activityprofile"
        ]:
            return ["dataquality/test_activity.html"]
        return ["dataquality/test_detail.html"]


class QualityAssuranceObjects(View):
    def get(self, req, *args: Any, **kwargs: Dict[str, str]) -> JsonResponse:

        cat = kwargs["category"]
        nick = kwargs["nickname"]

        user_org = Organisation.objects.filter(users__user=self.request.user).first()

        try:
            test = test_models(user_org)[cat][nick]  # type: TestModel
        except KeyError:
            raise KeyError("Invalid test name")

        objects = test.objects.all()

        if cat in [
            "activity",
            "activity_organisations",
            "activity_transactions",
            "sectors_and_coordination_bodies",
            "locations",
            "activityprofile"
        ]:
            serializer = ActivitySerializer
            try:
                if req.user.is_superuser:
                    content = {
                        "activities": serializer(
                            objects.filter(openly_status="published").distinct("id"),
                            many=True,
                        ).data
                    }
                elif user_org:
                    content = {
                        "activities": serializer(
                            objects.filter(openly_status="published")
                            .filter(reporting_organisation=user_org)
                            .distinct("id"),
                            many=True,
                        ).data
                    }
            except (NotImplementedError, AttributeError):
                #  "annotate() + distinct(fields) is not implemented" error
                if req.user.is_superuser:
                    content = {
                        "activities": serializer(
                            objects.filter(openly_status="published"), many=True
                        ).data
                    }
                elif user_org:
                    content = {
                        "activities": serializer(
                            objects.filter(openly_status="published").filter(
                                reporting_organisation=user_org
                            ),
                            many=True,
                        ).data
                    }
                else:
                    content = {}

            return JsonResponse(content)

        raise NotImplementedError("Not implemented yet")


class QualityAssuranceExport(ExportActivities):
    raw_sql = False
    exclude_pks = True

    def __init__(self, *args, **kwargs):
        super(QualityAssuranceExport, self).__init__(*args, **kwargs)

    @property
    def cache(self):
        return None

    def activity_hyperlink(self, instance: Dict, field: str) -> str:
        """
        Returns the hyperlink to activity edtitor page
        """
        protocol = "https"
        url = reverse("edit_activity", kwargs={"pk": instance[field]})
        return "%s://%s%s" % (protocol, self.domain, url)

    field_format_functions = {"pk": activity_hyperlink}

    def _get_test(self):
        return TestModel.get_test(
            self.kwargs.get("category", "activity"),
            self.kwargs.get("nickname"),
            user=self.request.user,
        )

    def get_filename(self) -> str:
        return "Data Quality %s" % (self._get_test().nickname)

    def get_queryset(self) -> QuerySet:
        return self._get_test().objects.annotate(**self.get_annotations())

    query_filters = (
        QueryFilter(
            param="org",
            field="reporting_organisation__abbreviation",
            description="Reporting Organisation's abbreviation",
        ),
        QueryFilter(
            param="org_id",
            field="reporting_organisation__code",
            description="Reporting Organisation's id",
        ),
    )

    def get_fields(self):
        return """
            id
            pk
            iati_identifier
            default_currency
            _hierarchy
            last_updated_datetime
            _linked_data_uri
            reporting_organisation
            reporting_organisation__name
            reporting_organisation__abbreviation
        """.split()


class TransactionQualityAssuranceExport(ExportTransactions):
    raw_sql = False
    exclude_pks = True

    def __init__(self, *args, **kwargs):
        super(TransactionQualityAssuranceExport, self).__init__(*args, **kwargs)

    @property
    def cache(self):
        return None

    def activity_hyperlink(self, instance: Dict, field: str) -> str:
        """
        Returns the hyperlink to activity edtitor page
        """
        protocol = "https"
        url = reverse("edit_activity", kwargs={"pk": instance[field]})
        return "%s://%s%s" % (protocol, self.domain, url)

    field_format_functions = {"activity_id": activity_hyperlink}

    def _get_test(self):
        return TestModel.get_test(
            "transaction", self.kwargs.get("nickname"), user=self.request.user
        )

    def get_filename(self) -> str:
        return "Data Quality %s" % (self._get_test().nickname)

    def get_queryset(self) -> QuerySet:
        return self._get_test().objects.annotate(**self.get_annotations())

    query_filters = (
        QueryFilter(
            param="org",
            field="activity__reporting_organisation__abbreviation",
            description="Reporting Organisation's abbreviation",
        ),
        QueryFilter(
            param="org_id",
            field="activity__reporting_organisation__code",
            description="Reporting Organisation's id",
        ),
    )

    def get_fields(self):
        return """
            activity_id
            currency
            transaction_date
            value_date
            activity__reporting_organisation__name
            provider_organisation__name
            receiver_organisation__name
        """.split()
