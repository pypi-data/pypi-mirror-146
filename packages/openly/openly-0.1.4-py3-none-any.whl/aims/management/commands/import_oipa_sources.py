from django.core.management.base import BaseCommand

from aims.synchronization.oipa_syncer import IATISourceSyncer


class Command(BaseCommand):
    help = 'Imports all known OIPA source document definitions from OIPA - does not parse those documents'

    def add_arguments(self, parser):
        parser.add_argument('--oipa', default='', help='The domain of the OIPA API')

    def handle(self, *args, **options):
        syncer = IATISourceSyncer(options['oipa'])
        syncer.sync()
