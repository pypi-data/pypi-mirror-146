from django.core.management.base import BaseCommand

from aims.synchronization.oipa_syncer import OipaSyncer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--reported_by', action='append', type=str)
        parser.add_argument('--activities', action='append', type=str)
        parser.add_argument('--since', action='store', type=str)
        parser.add_argument('--xml', action='store', type=str)

    def handle(self, *args, **options):
        oipa_syncer = OipaSyncer(
            reporting_organisations=options.get('reported_by', None),
            activities=options.get('activities', None),
            since=options.get('since', None),
            xml=options.get('xml', None)
        )
        oipa_syncer.sync()
