# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.db.migrations import SeparateDatabaseAndState, DeleteModel


class Migration(migrations.Migration):

    dependencies = [('aims', '0040_move_organisationrole_aims'), ('iati', '0019_aimsy_organisationroles')]
    operations = [
        migrations.AlterField(
            model_name='activityparticipatingorganisation',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aims.OrganisationRole'),
            preserve_default=True,
        ),

        migrations.AlterField(
            model_name='description',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aims.Language'),
        ),
        migrations.AlterField(
            model_name='documentlink',
            name='language',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='aims.Language'),
        ),
        migrations.AlterField(
            model_name='title',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aims.Language'),
        ),

        SeparateDatabaseAndState(None, [
            DeleteModel('OrganisationRole'),
            DeleteModel('Language')
        ])
    ]
