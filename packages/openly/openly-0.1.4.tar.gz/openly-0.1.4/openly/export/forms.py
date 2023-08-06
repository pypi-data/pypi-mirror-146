from django import forms
from django.utils.translation import gettext_lazy as _

from aims.models import Sector, Organisation

from aims import common_text
from aims.forms import FilterForm


REPORT_CHOICES = (('donor_summary', _('Donor Summary Report')),
                  ('sector_summary', _('Sector Summary Report')),
                  ('development_partner_report', _('Development Partner Report')),
                  ('sector_report', _('Sector Report')),
                  ('location_report', _('Location Report')),
                  ('activity_annual_breakdown', _('Annual Breakdown By Activity')),
                  ('dp_annual_breakdown', _('Annual Breakdown By Development Partner')),
                  #   ('state_annual_breakdown', _('Annual Breakdown By State/Region')),
                  #   ('township_annual_breakdown', _('Annual Breakdown By Township')),
                  ('sector_annual_breakdown', _('Annual Breakdown By Sector')),
                  ('dp_quarterly_breakdown', _('Quarterly Breakdown By Development Partner')),
                  ('state_quarterly_breakdown', _('Quarterly Breakdown By State/Region')),
                  ('township_quarterly_breakdown', _('Quarterly Breakdown By Township')),
                  ('sector_quarterly_breakdown', _('Quarterly Breakdown By Sector')),
                  ('sector_working_group', common_text.get('non_iati_sector_object_report')),
                  ('development_partner_profile', _('Development Partner Profiles')),
                  ('data_quality', _('Data Quality')),
                  )

DATA_QUALITY_TYPES = (('activities_without_date', _('Activities Without Dates')),
                      ('activities_absent_dashboard', _('Activities Absent From The Dashboard')),
                      ('activities_without_transaction', _('Activities Without Transactions')),
                      ('activities_without_commitment', _('Activities Without Commitments')),
                      ('activities_without_budget', _('Activities Without Budgets')),
                      )

MISSING_DATES_TYPES = (('start_actual', _('No Actual Start Date')),
                       ('end_actual', _('No Actual End Date')),
                       ('start_planned', _('No Planned Start Date')),
                       ('end_planned', _('No Planned End Date')),
                       )


class ExportForm(FilterForm):
    """ Form used by ExportView for filtering Activity and Transaction objects

    In addition to the base filter parameters inherited from FilterForm, some export types allow
    filtering by the reporting organisation or by the sector working group. The report type is
    used to distinguish what type of export to generate.
    """
    report_type = forms.ChoiceField(choices=REPORT_CHOICES)
    data_quality_type = forms.ChoiceField(choices=DATA_QUALITY_TYPES, required=False)
    development_partner = forms.ModelChoiceField(Organisation.objects.filter(activity_reporting_organisation__isnull=False).distinct().order_by('name'), required=False)
    sector_working_group = forms.ModelChoiceField(Sector.objects.filter(activitysector__vocabulary='RO').distinct().order_by('name'), required=False)
    missing_dates = forms.MultipleChoiceField(choices=MISSING_DATES_TYPES, widget=forms.CheckboxSelectMultiple, required=False)

    def clean(self):
        cleaned_data = super(ExportForm, self).clean()
        report_type = cleaned_data.get('report_type')
        if report_type == 'sector_report' and cleaned_data.get('sector') is None:
            self.add_error('sector', ['This field is required for a Sector Report.'])
        elif report_type == 'location_report' and cleaned_data.get('state') is None:
            self.add_error('state', ['This field is required for a Location Report.'])
        elif (report_type == 'development_partner_report' and cleaned_data.get('development_partner') is None):
            self.add_error('development_partner', ['This field is required for a Development Partner Report.'])
        elif (report_type == 'sector_working_group' and cleaned_data.get('sector_working_group') is None):
            self.add_error('sector_working_group', ['This field is required for a {object} Report'.format(object=common_text.get('non_iati_sector_object'))])
        elif (report_type == 'data_quality' and
              cleaned_data.get('data_quality_type') == 'activities_without_date' and
              not cleaned_data.get('missing_dates')):
            self.add_error('missing_dates', ['This field is required for an Activities Without Dates report'])

        return cleaned_data
