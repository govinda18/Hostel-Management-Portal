# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-01 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostel_name', models.CharField(max_length=1000)),
                ('location', models.CharField(max_length=1000)),
                ('rooms', models.PositiveIntegerField(default=0)),
                ('hostel_image1', models.ImageField(upload_to='hostel_images')),
                ('hostel_image2', models.ImageField(upload_to='hostel_images')),
                ('hostel_image3', models.ImageField(upload_to='hostel_images')),
            ],
        ),
    ]
