# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-30 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0027_auto_20180814_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='eligibility_tests',
            field=models.CharField(blank=True, default='HAAD', max_length=500),
        ),
    ]
