# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-03 16:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0011_exam_advertisement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='hall_ticket_download_minimum_number_of_days',
        ),
        migrations.AddField(
            model_name='exam',
            name='hall_ticket_download_last_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
