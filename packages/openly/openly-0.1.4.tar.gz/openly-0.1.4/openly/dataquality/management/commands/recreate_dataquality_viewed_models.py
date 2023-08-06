from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

REVISION = 3  # Increment this to determine where in the migrations run the views ought to be (re-)created


class Command(BaseCommand):
    help = 'Recreates the views found in dataquality models'

    def add_arguments(self, parser):
        parser.add_argument('--revision', default='1', help='The revision number to run')

    def handle(self, *args, **options):

        return False
