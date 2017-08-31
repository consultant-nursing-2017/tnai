# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-30 12:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_auto_20170830_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='candidate_username',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_username', to=settings.AUTH_USER_MODEL),
        ),
    ]
