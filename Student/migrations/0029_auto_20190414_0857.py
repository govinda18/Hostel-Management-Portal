# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-14 08:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0028_auto_20190414_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grievance',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 4, 14, 8, 57, 16, 807295)),
        ),
        migrations.AlterField(
            model_name='lostfound',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 14, 8, 57, 16, 813017)),
        ),
        migrations.AlterField(
            model_name='notifcation',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 14, 8, 57, 16, 803751)),
        ),
    ]