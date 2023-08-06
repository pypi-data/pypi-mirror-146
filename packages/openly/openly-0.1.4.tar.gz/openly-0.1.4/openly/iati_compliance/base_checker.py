from django.utils.translation import ugettext as _
from django.db import models
import dateutil.parser
import datetime
import re


class ComplianceCheckerMessages(object):
    """ Validation messages used by the base compliance checker """

    MISSING = _("This field is required")
    DATE_PARSE_ERROR = _("This value fails to parse as a date")
    DATE_NOT_PAST = _("This value must be a date in the past")
    REGEX_FAILS = _("This value has characters iati does not accept (/&|?)")


class ComplianceChecker(object):
    '''Base class for conpliance checkers - provides validation store'''

    IATI_REGEX = re.compile(r'^[^\/\&\|\?]+$')

    def __init__(self, model_to_check=None, *args, **kwargs):
        self._errors = []
        if not isinstance(model_to_check, models.Model):
            raise TypeError("This class expects a django model instance")
        self.model_to_check = model_to_check
        self.fields = get_model_fields(self.model_to_check)

    def is_compliant(self):
        '''Is the object to check compliant with IATI 2.01'''

        self._errors = []
        self.check()
        return len(self._errors) == 0

    def check(self):
        '''checks the given object for compliance - should be overridden in sub-classes'''

        raise NotImplementedError("A compliance check for this checker has not been written yet")

    def date_string_field_valid(self, field_name, required=True, past_check=True):
        '''checks a given string date field'''

        field, value = self._get_field_and_value(field_name)
        if not isinstance(field, models.CharField):
            raise TypeError("This method expects the name of a model char field")
        if len(value) > 0:
            try:
                date = dateutil.parser.parse(value)
                if past_check and date > datetime.datetime.now():
                    self.add_error(field, ComplianceCheckerMessages.DATE_NOT_PAST)
                    return False
            except ValueError:
                self.add_error(field, ComplianceCheckerMessages.DATE_PARSE_ERROR)
                return False
        else:
            if required:
                self.add_error(field, ComplianceCheckerMessages.MISSING)
                return False

        return True

    def field_not_empty(self, field_name):
        '''checks a field is not empty'''

        field, value = self._get_field_and_value(field_name)
        if isinstance(value, str) and (value is None or len(value) == 0):
            self.add_error(field, ComplianceCheckerMessages.MISSING)
            return False
        elif value is None:
            self.add_error(field, ComplianceCheckerMessages.MISSING)
            return False
        return True

    def iati_regex_valid(self, field_name):
        '''checks a field value matches the iati regex'''

        field, value = self._get_field_and_value(field_name)
        if re.match(ComplianceChecker.IATI_REGEX, value) is None:
            self.add_error(field, ComplianceCheckerMessages.REGEX_FAILS)
            return False
        return True

    def add_error(self, field, error_msg):
        '''Adds an error to the internal error list'''

        self._errors.append((field, error_msg))

    def _get_field_and_value(self, field_name):
        '''returns a tuple of filed and value on the object being checked from a given field name'''

        return (self._field(field_name), getattr(self.model_to_check, field_name, ''))

    def _field(self, name):
        '''Get a named model field from the object to be checked'''

        return self.fields[name]


def get_model_fields(model):
    ''' Returns all fields from a django model instance'''

    fields = {}
    options = model._meta
    for field in sorted(options.concrete_fields + options.many_to_many + options.virtual_fields):
        fields[field.name] = field
    return fields
