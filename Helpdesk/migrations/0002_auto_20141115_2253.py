# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='responseDesc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='response',
            name='status',
            field=models.CharField(default='Open', max_length=255, choices=[('Responded', 'Responded'), ('Fixed', 'Fixed'), ('Reopen', 'Reopen'), ('Close', 'Close'), ('Canceled', 'Canceled')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='problemDesc',
            field=models.TextField(max_length=999),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='stepToReproduce',
            field=models.TextField(max_length=999),
        ),
        migrations.AlterField(
            model_name='tickethistory',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tickethistory',
            name='remark',
            field=models.TextField(),
        ),
    ]
