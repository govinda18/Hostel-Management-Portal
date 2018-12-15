# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-15 16:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0015_auto_20181215_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_code', models.CharField(max_length=50)),
                ('expiry', models.DateField()),
                ('profile_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Student.Profile')),
            ],
        ),
        migrations.AlterField(
            model_name='grievance',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 15, 16, 24, 15, 71045)),
        ),
        migrations.AlterField(
            model_name='notifcation',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 15, 16, 24, 15, 68510)),
        ),
    ]
