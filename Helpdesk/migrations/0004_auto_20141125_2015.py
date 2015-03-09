# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Helpdesk', '0003_response_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='solutionDesc',
            field=models.TextField(blank=True, max_length=999, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='response',
            name='status',
            field=models.CharField(choices=[('Responded', 'Responded'), ('Fixed', 'Fixed'), ('Reopen', 'Reopen'), ('Closed', 'Closed'), ('Canceled', 'Canceled')], max_length=255, default='Open'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('', ''), ('Open', 'Open'), ('Assigned', 'Assigned'), ('Responded', 'Responded'), ('Fixed', 'Fixed'), ('Reopen', 'Reopen'), ('Closed', 'Closed'), ('Canceled', 'Canceled')], max_length=255, default='Open'),
        ),
    ]
