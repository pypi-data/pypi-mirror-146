from django.core.management.base import BaseCommand

from aims.models import Activity


class Command(BaseCommand):
    help = 'Calculate (and store) completion ratio for activities.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Recalculate for *all* activities, not just the ones for which it is currently unknown.')

    def handle(self, *args, **options):
        acts = Activity.objects.all_openly_statuses() if options['all'] else Activity.objects.all_openly_statuses().filter(completion=None)
        tot_cnt = acts.count()
        for cnt, act in enumerate(acts):
            act.save()  # this triggers a recalculation through a signal
            if (cnt % 100 == 0) and (options['verbosity'] >= 2):
                print('%d/%d' % (cnt, tot_cnt))
