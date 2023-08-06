from django.test import TestCase
from django.db import models
from .base_checker import ComplianceChecker, ComplianceCheckerMessages
from .activity import ActivityChecker, ActivityCheckerMessages
from aims import models as aims
import datetime


class CheckerTestCase(TestCase):
    """ Base class for checker tests """

    def assert_has_error(self, checker, field_name, error, only=True):
        if only:
            self.assertEqual(len(checker._errors), 1, "More than one error was found")
        found = False
        for field, err in checker._errors:
            if field.attname == field_name and error == err:
                found = True
        self.assertEqual(found, True, "The expected error was not found")


class ActivityCheckerTests(CheckerTestCase):
    '''Tests for ActivityChecker'''

    fixtures = ['iati_objects_required.json']

    @classmethod
    def setUpClass(cls):
        aims.Language.objects.create(
            code='en',
            name='English'
        )

    def setUp(self):
        self.compliant_activity = self._get_compliant_activity()

    def _get_compliant_activity(self):
        org = aims.Organisation.objects.create(
            code='org'
        )
        activity = aims.Activity.objects.create(
            last_updated_datetime=datetime.datetime.now().isoformat(),
            iati_identifier='org-id',
            reporting_organisation=org
        )
        return activity

    def test_activity_compliant(self):
        '''The compliant activity is indeed compliant'''

        checker = ActivityChecker(self.compliant_activity)
        self.assertEqual(checker.is_compliant(), True)

    def test_activity_without_last_updated(self):
        '''Tests that an activity without a last_updated_datetime fails validation'''

        activity = self.compliant_activity
        activity.last_updated_datetime = ''
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)
        self.assert_has_error(checker, 'last_updated_datetime', ComplianceCheckerMessages.MISSING)

    def test_activity_without_iati_identifier(self):
        '''Tests that an activity without an iati identifier fails validation'''

        activity = self.compliant_activity
        activity.iati_identifier = ''
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)
        self.assert_has_error(checker, 'iati_identifier', ActivityCheckerMessages.IATI_IDENTIFIER_FORMAT)

    def test_activity_with_bad_iati_identifier(self):
        '''Tests that an activity with an invalid iati identifier fails validation'''

        activity = self.compliant_activity
        activity.iati_identifier = '?ddd'
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)
        self.assert_has_error(checker, 'iati_identifier', ActivityCheckerMessages.IATI_IDENTIFIER_FORMAT)

    def test_activity_with_iati_identifier_different_to_reportingorg(self):
        '''Tests that an activity with an iati identifier different to it's reporting org fails validation'''

        activity = self.compliant_activity
        activity.reporting_organisation.code = 'notorg'
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)
        self.assert_has_error(checker, 'iati_identifier', ActivityCheckerMessages.IATI_ORGANISATION_MATCH)

    def test_activity_with_iati_identifier_in_other_identier(self):
        '''Tests that an activity with an iati identifier different to it's reporting org but in an other identifier passes validation'''

        activity = self.compliant_activity
        activity.reporting_organisation.code = 'notorg'
        other_identifier = aims.OtherIdentifier(owner_ref='org')

        activity.otheridentifier_set.add(
            other_identifier
        )
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), True)

    def test_activity_with_iati_identifier_not_in_other_identier(self):
        '''Tests that an activity with an iati identifier different to it's reporting org and not in an other identifier fails validation'''

        activity = self.compliant_activity
        activity.reporting_organisation.code = 'notorg'
        other_identifier = aims.OtherIdentifier(owner_ref='notnotorg')

        activity.otheridentifier_set.add(
            other_identifier
        )
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)
        self.assert_has_error(checker, 'iati_identifier', ActivityCheckerMessages.IATI_ORGANISATION_MATCH)

    def test_activity_without_title_fails(self):
        ''' An activity without a title should fail compliance check '''

        activity = self.compliant_activity
        activity.title_set.all().delete()
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)

    def test_activity_with_title_without_lang_fails(self):
        ''' An activity without a title should fail compliance check '''

        activity = self.compliant_activity
        title = activity.title_set.first()
        title.language_id = None
        title.save()
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)

    def test_activity_without_description_fails(self):
        ''' An activity without a description should fail compliance check '''

        activity = self.compliant_activity
        activity.description_set.all().delete()
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)

    def test_activity_with_description_without_lang_fails(self):
        ''' An activity without a description should fail compliance check '''

        activity = self.compliant_activity
        description = activity.description_set.first()
        description.language_id = None
        description.save()
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)

    def test_activity_with_multiple_descriptions_without_type(self):
        ''' An activity without a description should fail compliance check '''

        activity = self.compliant_activity
        description = aims.Description.objects.create(
            activity_id=activity.pk,
            description='Description 2',
            language_id='en'
        )
        description.save()
        checker = ActivityChecker(activity)
        self.assertEqual(checker.is_compliant(), False)


class TestModel(models.Model):
    '''A Test model to use in compliance checker tests'''

    test_text = models.CharField(max_length=100, default="")


class ComplianceCheckerTests(CheckerTestCase):
    '''Tests for base compliance methods'''

    def test_iati_regex_valid_ok(self):
        """ IATI regex check should pass with a valid identifier """

        test_model = TestModel(test_text='ofwoeufhew-wfwefwe2')
        checker = ComplianceChecker(test_model)
        self.assertEqual(True, checker.iati_regex_valid("test_text"))
        self.assertEqual(len(checker._errors), 0)

    def test_iati_regex_valid_fails(self):
        """ IATI regex check should fail with an invalid identifier """

        test_model = TestModel(test_text='ofwoe?uf|hew-wfwe/fwe2')
        checker = ComplianceChecker(test_model)
        self.assertEqual(False, checker.iati_regex_valid("test_text"))
        self.assert_has_error(checker, 'test_text', ComplianceCheckerMessages.REGEX_FAILS, only=True)

    def test_field_not_empty_fails(self):
        """ Field empty check should fail with an empty field """

        test_model = TestModel(test_text='')
        checker = ComplianceChecker(test_model)
        self.assertEqual(False, checker.field_not_empty("test_text"))
        self.assert_has_error(checker, 'test_text', ComplianceCheckerMessages.MISSING, only=True)

    def test_field_not_empty_ok(self):
        """ Filed empty check should pass with a non-empty field """

        test_model = TestModel(test_text='fff')
        checker = ComplianceChecker(test_model)
        self.assertEqual(True, checker.field_not_empty("test_text"))

    def test_date_string_field_valid_empty_fails(self):
        """ String date field check should fail with an empty field """

        test_model = TestModel(test_text='')
        checker = ComplianceChecker(test_model)
        self.assertEqual(False, checker.date_string_field_valid("test_text"))
        self.assert_has_error(checker, 'test_text', ComplianceCheckerMessages.MISSING, only=True)

    def test_date_string_field_invalid_fails(self):
        """ String date field check should fail with a string that does not parse as a date """

        test_model = TestModel(test_text='jbjbwle')
        checker = ComplianceChecker(test_model)
        self.assertEqual(False, checker.date_string_field_valid("test_text"))
        self.assert_has_error(checker, 'test_text', ComplianceCheckerMessages.DATE_PARSE_ERROR, only=True)

    def test_date_string_field_future_fails(self):
        """ String date field check should fail with future date """

        tomorrow = datetime.datetime.now() + datetime.timedelta(1)
        test_model = TestModel(test_text=tomorrow.isoformat())
        checker = ComplianceChecker(test_model)
        self.assertEqual(False, checker.date_string_field_valid("test_text"))
        self.assert_has_error(checker, 'test_text', ComplianceCheckerMessages.DATE_NOT_PAST, only=True)

    def test_date_string_field_future_ok(self):
        """ String date field check should pass with a future date if past_check is false """

        tomorrow = datetime.datetime.now() + datetime.timedelta(1)
        test_model = TestModel(test_text=tomorrow.isoformat())
        checker = ComplianceChecker(test_model)
        self.assertEqual(True, checker.date_string_field_valid("test_text", past_check=False))

    def test_date_string_field_ok(self):
        """ String date field check should pass with a past date """

        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        test_model = TestModel(test_text=yesterday.isoformat())
        checker = ComplianceChecker(test_model)
        self.assertEqual(True, checker.date_string_field_valid("test_text"))

    def test_date_string_field_ok_empty(self):
        """ String date field check should pass with an empty date if required is false """

        test_model = TestModel(test_text='')
        checker = ComplianceChecker(test_model)
        self.assertEqual(True, checker.date_string_field_valid("test_text", required=False))
