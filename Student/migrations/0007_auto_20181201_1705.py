# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-01 17:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0006_auto_20181201_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='notifcation',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 1, 17, 5, 53, 355919)),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
