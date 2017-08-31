# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-30 12:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0004_auto_20170830_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='candidate_username',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_username', to=settings.AUTH_USER_MODEL),
        ),
    ]
