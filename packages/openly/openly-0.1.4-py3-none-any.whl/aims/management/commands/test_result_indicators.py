from django.core.management.base import BaseCommand
from aims import models as aims


class Command(BaseCommand):
    help = 'Quick and dirty test of  ResultIndicators'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        indicator = aims.ResultIndicator.objects.first()

        for group, name in (
            ('gender', 'gender'),
            ('time', 'quarterly'),
            ('time', 'monthly'),
            ('time', 'day'),
            ('time', 'year'),
        ):

            aims.ResultIndicatorDimensionType.objects.get_or_create(group=group, name=name)

        # Narrative type
        aims.ResultIndicatorDimension(
            indicator=indicator,
            results="Hello World"
        ).save()

        #
        aims.ResultIndicatorDimension(
            indicator=indicator,
            dim=aims.ResultIndicatorDimensionType.objects.get(name='gender'),
            dim_2=None,
            stores='text',
            results={'M': "hello", 'F': "I'm a number"}
        ).save()

        results_gender_quarter = {
            'M': {
                '2017_Q1': 1,
                '2018_Q2': 2
            },
            'F': {
                '2017_Q1': 1,
                '2018_Q2': 2
            }
        }

        aims.ResultIndicatorDimension(
            indicator=indicator,
            dim=aims.ResultIndicatorDimensionType.objects.get(name='gender'),
            dim_2=aims.ResultIndicatorDimensionType.objects.get(name='quarterly'),
            stores='num',
            results=results_gender_quarter
        ).save()

        results_gender_month = {
            'M': {
                '2017_01': 1,
                '2018_08': 2
            },
            'F': {
                '2017_05': 1,
                '2018_08': 2,
                '2020_09': 4
            }
        }

        aims.ResultIndicatorDimension(
            indicator=indicator,
            dim=aims.ResultIndicatorDimensionType.objects.get(name='gender'),
            dim_2=aims.ResultIndicatorDimensionType.objects.get(name='monthly'),
            stores='num',
            results=results_gender_month
        ).save()
