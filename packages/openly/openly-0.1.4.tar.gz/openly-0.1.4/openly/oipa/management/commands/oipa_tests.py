from django.core.management.base import BaseCommand
from oipa.services import OipaRecords

test_iati_ids = [
    'XI-IATI-EC_DEVCO_T05-EUTF-REG-REG-01',  # Failed with a 404 from /transactions
    'XI-IATI-EC_DEVCO-2015/353-196',  # Failed with a TypeError due to having a budget with null value
    'NL-KVK-27264198_AA-Myanmar_BRC/10601',  # Failed with a KeyError
    'XM-OCHA-FTS-MM-14/CSS/78619/R/120',  # This one
    'NL-KVK-27264198_AA-Myanmar_RRP/10173',
    'XM-DAC-701-8-2014003081',      # As reported by Leigh
    'CA-3-D004240001',
]


class Command(BaseCommand):
    help = 'Try some IATI imports which have previously been problematic'

    def handle(self, *args, **options):
        for iati_identifier in test_iati_ids:
            records = OipaRecords(iati_id=iati_identifier)
            records.get_activity()
            records.get_transactions()
            records.get_budgets()
