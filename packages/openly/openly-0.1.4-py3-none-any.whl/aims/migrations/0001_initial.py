# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0002_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('openly_status', models.CharField(default=b'iatixml', max_length=12, choices=[(b'iatixml', 'Found in iati XML, hidden from dashboards'), (b'draft', 'Draft, visible in organisation login activity lists, hidden from dashboards'), (b'published', 'Published, publicly visible on dashbaords')])),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Activity', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activity', models.Model),
        ),
        migrations.CreateModel(
            name='ActivityParticipatingOrganisation',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ActivityParticipatingOrganisation', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activityparticipatingorganisation', models.Model),
        ),
        migrations.CreateModel(
            name='ActivityPolicyMarker',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ActivityPolicyMarker', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activitypolicymarker', models.Model),
        ),
        migrations.CreateModel(
            name='ActivityRecipientCountry',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ActivityRecipientCountry', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activityrecipientcountry', models.Model),
        ),
        migrations.CreateModel(
            name='ActivityRecipientRegion',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ActivityRecipientRegion', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activityrecipientregion', models.Model),
        ),
        migrations.CreateModel(
            name='ActivitySector',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ActivitySector', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activitysector', models.Model),
        ),
        migrations.CreateModel(
            name='ActivityTotalBudgetUSD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dollars', models.FloatField(null=True, blank=True)),
                ('activity', models.OneToOneField(related_name='total_budget_in', verbose_name=b'Activity Budget in USD', to='iati.Activity', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'aims_activity_total_budget_usd',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityWebsite',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ActivityWebsite', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.activitywebsite', models.Model),
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Budget', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.budget', models.Model),
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Condition', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.condition', models.Model),
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ContactInfo', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.contactinfo', models.Model),
        ),
        migrations.CreateModel(
            name='CurrencyExchangeRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.DecimalField(verbose_name='Exchange Rate', max_digits=16, decimal_places=8)),
                ('date', models.DateField()),
                ('base_currency', models.ForeignKey(related_name='base_currencies', verbose_name='Base Currency', to='iati.Currency', on_delete=django.db.models.deletion.CASCADE)),
                ('currency', models.ForeignKey(related_name='exchange_currencies', verbose_name='Exchange Currency', to='iati.Currency', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'aims_currency_exchange_rate',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Description', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.description', models.Model),
        ),
        migrations.CreateModel(
            name='DocumentLink',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.DocumentLink', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.documentlink', models.Model),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Location', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.location', models.Model),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Organisation', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.organisation', models.Model),
        ),
        migrations.CreateModel(
            name='OtherIdentifier',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.OtherIdentifier', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.otheridentifier', models.Model),
        ),
        migrations.CreateModel(
            name='PlannedDisbursement',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.PlannedDisbursement', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.planneddisbursement', models.Model),
        ),
        migrations.CreateModel(
            name='RelatedActivity',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.RelatedActivity', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.relatedactivity', models.Model),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Result', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.result', models.Model),
        ),
        migrations.CreateModel(
            name='ResultIndicator',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ResultIndicator', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.resultindicator', models.Model),
        ),
        migrations.CreateModel(
            name='ResultIndicatorPeriod',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ResultIndicatorPeriod', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.resultindicatorperiod', models.Model),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Sector', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.sector', models.Model),
        ),
        migrations.CreateModel(
            name='SectorCategory',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.SectorCategory', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.sectorcategory', models.Model),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Title', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.title', models.Model),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('openly_status', models.CharField(default=b'iatixml', max_length=12, choices=[(b'iatixml', 'Found in iati XML, hidden from dashboards'), (b'draft', 'Draft, visible in organisation login activity lists, hidden from dashboards'), (b'published', 'Published, publicly visible on dashbaords')])),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Transaction', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.transaction', models.Model),
        ),
        migrations.CreateModel(
            name='TransactionValueLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(null=True, blank=True)),
                ('dollars', models.FloatField(null=True, blank=True)),
                ('activity', models.ForeignKey(related_name='transaction_value_for_location', blank=True, to='iati.Activity', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('currency', models.ForeignKey(blank=True, to='iati.Currency', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('location', models.ForeignKey(related_name='transaction_value_for_location', blank=True, to='iati.Location', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('transaction', models.ForeignKey(related_name='transaction_value_for_location', blank=True, to='iati.Transaction', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'aims_transaction_value_location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionValueUSD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dollars', models.FloatField(null=True, blank=True)),
                ('rate', models.ForeignKey(blank=True, to='aims.CurrencyExchangeRate', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('transaction', models.OneToOneField(related_name='value_in', verbose_name=b'Transaction Value in USD', to='iati.Transaction', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'aims_transaction_value_usd',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserOrganisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organisations', models.ManyToManyField(related_name='users', null=True, to='iati.Organisation', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueType',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.ValueType', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.valuetype', models.Model),
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('date_created', models.DateField(null=True, verbose_name='Date Created', blank=True)),
                ('date_modified', models.DateField(null=True, verbose_name='Last Modified', blank=True)),
                ('remote_data', models.OneToOneField(parent_link=True, related_name='local_data', primary_key=True, serialize=False, to='iati.Vocabulary', verbose_name='Remote Data', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('iati.vocabulary', models.Model),
        ),
        migrations.AddField(
            model_name='activitytotalbudgetusd',
            name='rate',
            field=models.ForeignKey(blank=True, to='aims.CurrencyExchangeRate', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
