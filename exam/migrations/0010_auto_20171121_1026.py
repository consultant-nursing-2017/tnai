# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0009_auto_20171121_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_type',
            field=models.CharField(blank=True, choices=[('Written + Interview', 'Written + Interview'), ('Only Interview', 'Only Interview')], default='Only Interview', max_length=100),
        ),
        migrations.AlterField(
            model_name='exam',
            name='hall_ticket_download_minimum_number_of_days',
            field=models.PositiveSmallIntegerField(blank=True, default=10, null=True),
        ),
    ]
