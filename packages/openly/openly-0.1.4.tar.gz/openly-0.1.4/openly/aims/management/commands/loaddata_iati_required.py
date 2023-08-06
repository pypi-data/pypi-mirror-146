from django.core.management import call_command
from django.core.management.base import BaseCommand

REVISION = '0042'  # Corresponding to the migration number to be imported at


class Command(BaseCommand):
    help = 'Loads the iati_objects_required fixture if called with the correct version number which is currently %s' % (REVISION)

    def add_arguments(self, parser):
        parser.add_argument('--revision', default='', help='The revision number to verify')

    def handle(self, *args, **options):
        if options['revision'] == REVISION:
            call_command('loaddata', 'iati_objects_required', app_label='aims')
