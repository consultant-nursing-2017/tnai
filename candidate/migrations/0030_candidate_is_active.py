# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-12 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0029_auto_20171124_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
