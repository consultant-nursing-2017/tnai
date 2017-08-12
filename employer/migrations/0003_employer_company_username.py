# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-01 08:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employer', '0002_remove_employer_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='company_username',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_username', to=settings.AUTH_USER_MODEL),
        ),
    ]
