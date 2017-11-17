# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-25 17:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0006_auto_20170925_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='employer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employer_advert', to='employer.Employer'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='closing_date',
            field=models.DateField(default=datetime.datetime(2017, 10, 25, 17, 43, 26, 205698, tzinfo=utc)),
        ),
    ]