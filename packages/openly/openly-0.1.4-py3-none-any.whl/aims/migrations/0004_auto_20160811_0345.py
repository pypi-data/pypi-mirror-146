# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0003_auto_20160405_1505'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.AlterField(
            model_name='userorganisation',
            name='organisations',
            field=models.ManyToManyField(related_name='users', to='iati.Organisation'),
        ),
    ]
