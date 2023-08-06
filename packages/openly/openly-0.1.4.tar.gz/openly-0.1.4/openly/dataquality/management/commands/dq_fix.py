from django.core.management.base import BaseCommand

from dataquality.automated_fixes import run_all
import logging

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    help = 'Run the "run_all" command in automated_fixes'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):

        run_all()
