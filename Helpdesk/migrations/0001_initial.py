# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssignTo',
            fields=[
                ('assignToId', models.AutoField(serialize=False, primary_key=True)),
                ('assignDateTime', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'AssignTo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocNumber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('docType', models.CharField(max_length=3)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('lastNumber', models.IntegerField()),
            ],
            options={
                'db_table': 'DocNumber',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('responseId', models.AutoField(serialize=False, primary_key=True)),
                ('responseDesc', models.CharField(max_length=999)),
                ('responseDateTime', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(default='Open', max_length=255, choices=[('', ''), ('Open', 'Open'), ('Assigned', 'Assigned'), ('Responded', 'Responded'), ('Fixed', 'Fixed'), ('Reopen', 'Reopen'), ('Close', 'Close'), ('Canceled', 'Canceled')])),
            ],
            options={
                'db_table': 'Response',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketId', models.AutoField(serialize=False, primary_key=True)),
                ('ticketNo', models.CharField(max_length=255, unique=True)),
                ('reportedDateTime', models.DateTimeField(default=datetime.datetime.now)),
                ('priority', models.CharField(default='Medium', max_length=255, choices=[('', ''), ('Critical', 'Critical'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])),
                ('problemType', models.CharField(default='Hardware', max_length=255, choices=[('', ''), ('Hardware', 'Hardware'), ('Software', 'Software')])),
                ('problemTitle', models.CharField(max_length=999)),
                ('problemDesc', models.CharField(max_length=999)),
                ('stepToReproduce', models.CharField(max_length=999)),
                ('telephone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('status', models.CharField(default='Open', max_length=255, choices=[('', ''), ('Open', 'Open'), ('Assigned', 'Assigned'), ('Responded', 'Responded'), ('Fixed', 'Fixed'), ('Reopen', 'Reopen'), ('Close', 'Close'), ('Canceled', 'Canceled')])),
            ],
            options={
                'db_table': 'Ticket',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('ticketHistoryId', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=999)),
                ('desc', models.CharField(max_length=999)),
                ('remark', models.CharField(max_length=999)),
                ('historyDateTime', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'TicketHistory',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('telpNo', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75)),
                ('gender', models.CharField(default='', max_length=255, choices=[('', ''), ('Male', 'Male'), ('Female', 'Female')])),
                ('position', models.CharField(default='', max_length=255, choices=[('', ''), ('Superadmin', 'Superadmin'), ('Helpdesk', 'Helpdesk'), ('User', 'User')])),
                ('is_active', models.BooleanField(default=True, choices=[(True, 'Active'), (False, 'Not Active')])),
                ('is_admin', models.BooleanField(default=False, choices=[('', ''), (True, 'Active'), (False, 'Not Active')])),
            ],
            options={
                'db_table': 'Users',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='historyBy',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='ticketId',
            field=models.ForeignKey(to='Helpdesk.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='reportedBy',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='responseBy',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='ticketId',
            field=models.ForeignKey(to='Helpdesk.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignto',
            name='assignBy',
            field=models.ForeignKey(related_name='fk_assign_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignto',
            name='assignTo',
            field=models.ForeignKey(related_name='fk_assign_to', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignto',
            name='ticketId',
            field=models.ForeignKey(to='Helpdesk.Ticket'),
            preserve_default=True,
        ),
    ]
