# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-29 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='candidate',
            name='district',
            field=models.CharField(choices=[('Married', 'Married'), ('Single', 'Single')], default='Single', max_length=200),
        ),
        migrations.AddField(
            model_name='candidate',
            name='email',
            field=models.CharField(default='nursing.consultant.2017@gmail.com', max_length=200),
        ),
        migrations.AddField(
            model_name='candidate',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=200),
        ),
        migrations.AddField(
            model_name='candidate',
            name='marital_status',
            field=models.CharField(choices=[('Married', 'Married'), ('Single', 'Single')], default='Single', max_length=200),
        ),
    ]
