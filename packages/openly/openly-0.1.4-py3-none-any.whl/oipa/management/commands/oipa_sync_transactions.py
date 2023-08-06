from django.core.management.base import BaseCommand
from oipa.models import OipaActivityLink
from oipa.services import OipaSync

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports all transactions from OIPA into Openly for linked Openly Activities'

    def handle(self, *args, **options):
        logger.info("~~~ Starting Oipa Sync All Activities ~~~")
        linked_activities = OipaActivityLink.objects.exclude(oipa_fields=[]).all()
        logger.info("Total activities to sync: %s" % len(linked_activities))
        oipa = OipaSync()
        for link in linked_activities:
            oipa.sync_activity(link)
