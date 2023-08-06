from django.core.management.base import BaseCommand

from aims.synchronization.oipa_syncer import IATIOrganisationSyncer


class Command(BaseCommand):
    help = 'Imports all known OIPA organisation from OIPA'

    def add_arguments(self, parser):
        parser.add_argument('--oipa', default='', help='The domain of the OIPA API')

    def handle(self, *args, **options):
        syncer = IATIOrganisationSyncer(options['oipa'])
        syncer.sync()
