# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Helpdesk', '0004_auto_20141125_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='attachment',
            field=models.FileField(upload_to='C:/xampp/htdocs/MyProject3/Helpdesk/Static/Upload', default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='attachment',
            field=models.FileField(upload_to='C:/xampp/htdocs/MyProject3/Helpdesk/Static/Upload', default=''),
            preserve_default=True,
        ),
    ]
