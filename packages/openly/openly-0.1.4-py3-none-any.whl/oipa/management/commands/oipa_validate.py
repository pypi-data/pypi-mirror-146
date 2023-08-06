from django.core.management.base import BaseCommand
from aims.models import Activity
from oipa.services import OipaValidator, OipaRecords

import csv


class Command(BaseCommand):
    help = 'Validate all activities from OIPA for a given Organisation ID. Ouputs as CSV'

    def add_arguments(self, parser):
        parser.add_argument('org', type=str, help='Openly Organisation ID to get activities')

    def handle(self, *args, **options):
        if options['org']:
            self.stdout.write("Fetching activities for: %s" % options['org'])
            results = {}
            # get all activities for an org
            activities = Activity.objects.all_openly_statuses().filter(reporting_organisation=options['org']).all()
            self.stdout.write("Total activities to validate: %s" % len(activities))
            counter = 0
            # for each activity attempt to pull OIPA data and attempt to validate
            for activity in activities:
                if activity.iati_identifier is None:
                    continue
                counter += 1
                # try to fetch OIPA records
                oipa_records = OipaRecords(activity.iati_identifier)
                oipa_activity = oipa_records.get_activity()
                # if did not get a NONE back from the OIPA fetch activity
                # then we can try to fetch transactions an budget records
                if oipa_activity:
                    self.stdout.write(activity.id + " (M) | (O) " + oipa_activity['iati_id'])
                    oipa_budgets = oipa_records.get_budgets()
                    oipa_trans = oipa_records.get_transactions()
                    oipa_validator = OipaValidator(activity)
                    oipa_validator.validate_budgets(oipa_budgets['data'])
                    oipa_validator.validate_transactions(oipa_trans)
                    # append stringified activity validation status pass/fail to the results dictionary
                    results[activity.id] = dict((k, str(v)) for k, v in oipa_validator.results.items())
                    results[activity.id]['iati_id'] = oipa_activity['iati_id']
                else:
                    results[activity.id] = {'iati_id': 'N/A', 'B': 'N/A', 'C': 'N/A', 'IF': 'N/A', 'OF': 'N/A'}
            # Output the results dict to a CSV / Excel / etc...
            fields = ['openly_id', 'iati_id', 'B', 'C', 'IF', 'OF']
            with open('iati_validation_output_' + options['org'] + '.csv', 'w', newline='') as f:
                w = csv.DictWriter(f, fields)
                w.writeheader()
                for k in results:
                    w.writerow({field: results[k].get(field) or k for field in fields})
            self.stdout.write(self.style.SUCCESS('Successfully pulled and attempted to validate all activities!'))
        else:
            self.stderr.write('Missing Openly Organisation ID!')
