# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-15 16:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0014_auto_20181203_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grievance',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 15, 16, 6, 0, 694722)),
        ),
        migrations.AlterField(
            model_name='notifcation',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 15, 16, 6, 0, 692180)),
        ),
    ]
