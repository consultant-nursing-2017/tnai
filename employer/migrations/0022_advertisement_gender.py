# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-12 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0021_auto_20171206_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='gender',
            field=models.CharField(choices=[('Any', 'Any'), ('Male', 'Male'), ('Female', 'Female')], default='Any', max_length=200),
        ),
    ]
