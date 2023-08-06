from django.utils.translation import ugettext as _
from .base_checker import ComplianceChecker
from aims.models import Activity
import re


class ActivityCheckerMessages(object):
    """ Validation messages used by the activity checker """

    IATI_IDENTIFIER_FORMAT = _("the iati identifier must be present and consist of two groups separated by a hyphen ( - )")
    IATI_ORGANISATION_MATCH = _("the iati identifier must matcch the reporting organisation or an other identifier in the activity")
    TITLE_REQUIRES_LANGUAGE = _("All activity titles must have a language")
    TITLE_MISSING = _("All activities must have titles")
    DESCRIPTION_REQUIRES_LANGUAGE = _("All activity descriptions must have a language")
    DESCRIPTION_MISSING = _("All activities must have descriptions")
    DESCRIPTION_REQURIES_TYPE = _("If an activity has multiple descriptions they must all have types")


class ActivityChecker(ComplianceChecker):
    '''Checks an Activity for IATI compliance'''

    def __init__(self, activity, *args, **kwargs):
        if not isinstance(activity, Activity):
            raise TypeError("This class only accepts activity objects")
        self.activity = activity
        super(ActivityChecker, self).__init__(activity, *args, **kwargs)

    def check(self):
        # check that the last_updated_datetime is present and in the past_check
        # TODO: enforce this via code
        '''
        The last date/time that the data for this specific activity was updated.
        This date must change whenever the value of any field changes.
        '''
        self.date_string_field_valid('last_updated_datetime')

        # check the language code is present - if not all narrative elements require lang fields
        # TODO: NOT SUPPORTED BY OIPA YET
        '''
        ISO 639-1 code specifying the default language used in narrative elements throughout the activity.
        If this is not declared then the xml:lang attribute MUST be specified for each narrative element.
        '''

        # check the default currency is present - if not must be declared on all monetary values
        # TODO: write later checks to enforce this
        '''
        Default ISO 4217 alphabetic currency code for all financial values in this activity report.
        If this is not declared then the currency attribute MUST be specified for all monetary values.
        '''
        # has_default_currency = self.activity.default_currency is not None

        # hierachy requires no checking it may be present, but is assumed to be 1 if not
        # TODO: check with OIPA  it currently supports only 1,2 iati supports 1,2,3
        '''
        The hierarchical level within the reporting organisation's subdivision of its units of aid.
        (eg activity = 1; sub-activity = 2; sub-sub-activity = 3).
        If hierarchy is not reported then 1 is assumed.
        If multiple levels are reported then, to avoid double counting, financial transactions
        should only be reported at the lowest hierarchical level.
        '''

        # linked_data_uri not required
        # TODO: we could check it is a valid URI format if present, see help in next line
        '''
        This attribute is a URI path upon which an activity identifier can be appended to get
        a dereferenceable URI for any activity contained within a file.
        '''

        # iati_identifier
        #
        '''
        This MUST be prefixed with EITHER the current IATI organisation identifier for the
        reporting organisation (reporting-org/@ref) OR a previous identifier reported in other-identifier,
        and suffixed with the organisation's own activity identifier.
        The prefix and the suffix should be separated by a hyphen '-'.
        '''
        # is present and has no bad chars
        IATI_REGEX = re.compile(r'^([^\/\&\|\?]+)-([^\/\&\|\?]+)$')
        ii_field, ii_value = self._get_field_and_value('iati_identifier')

        matches = re.match(IATI_REGEX, ii_value)
        if matches is None:
            self.add_error(ii_field, ActivityCheckerMessages.IATI_IDENTIFIER_FORMAT)
        else:
            org_code, id_ref = matches.groups()
            # check for match with reporting organisation code
            if org_code != self.activity.reporting_organisation.code:
                # check for a match with other_identifier
                found = False
                for identifier in self.activity.otheridentifier_set.all():
                    if identifier.owner_ref == org_code:
                        found = True
                if not found:
                    self.add_error(ii_field, ActivityCheckerMessages.IATI_ORGANISATION_MATCH)

        # reporting org
        '''
        All activities in an activity xml file must contain the same @ref AND this @ref must be the same
        as the iati-identifier recorded in the registry publisher record of the account under which this file is published.
        '''
        # TODO: check with OIPA about secondary_publisher
        self.field_not_empty('reporting_organisation')

        # title
        '''
        IATI: This element should occur once and only once (within each parent element).
        OIPA: there should be at least one title related to an activity, and it must have an associated language ( lack of activity default language )
        '''
        # should have a title
        if self.activity.title_set.count() == 0:
            self.add_error(self.activity.title_set, ActivityCheckerMessages.TITLE_MISSING)

        # title requires language
        for title in self.activity.title_set.all():
            if title.language is None:
                self.add_error(self.activity.title_set, ActivityCheckerMessages.TITLE_REQUIRES_LANGUAGE)

        # description
        '''
        IATI: This element should occur at least once (within each parent element).
        OIPA: there should be at least one description linked to an activity - if more than one, they require types
        '''
        # should have a description
        description_count = self.activity.description_set.count()
        if description_count == 0:
            self.add_error(self.activity.description_set, ActivityCheckerMessages.DESCRIPTION_MISSING)

        # description requires language
        for description in self.activity.description_set.all():
            if description.language is None:
                self.add_error(self.activity.description_set, ActivityCheckerMessages.DESCRIPTION_REQUIRES_LANGUAGE)
            if description_count > 1 and description.type is None:
                self.add_error(self.activity.description_set, ActivityCheckerMessages.DESCRIPTION_REQURIES_TYPE)

        # participating organisation
