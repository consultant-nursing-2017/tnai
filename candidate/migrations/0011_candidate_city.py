# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-11 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0010_auto_20170911_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='city',
            field=models.CharField(default='Delhi', max_length=200),
        ),
    ]
