# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Helpdesk', '0002_auto_20141115_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='remark',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
