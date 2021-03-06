# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-25 17:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_auto_20170925_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='ad_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='air_ticket_for_joining',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='air_ticket_for_vacation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='allowances',
            field=models.CharField(blank=True, default='Travel', max_length=500),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='annual_leave_days',
            field=models.IntegerField(blank=True, default=14),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='duration_of_assignment_number',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='duration_of_assignment_units',
            field=models.CharField(choices=[('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Years', 'Years')], default='Months', max_length=15),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='family_accomodation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='medical_facilities',
            field=models.CharField(blank=True, choices=[('Self', 'Self'), ('Family', 'Family'), ('None', 'None')], default='Self', max_length=15),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='other_notes',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='personal_accomodation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='salary_number',
            field=models.IntegerField(default=1200),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='salary_units',
            field=models.CharField(default='AED', max_length=20),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='visa_cost',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='closing_date',
            field=models.DateField(default=datetime.datetime(2017, 10, 25, 17, 15, 37, 341822, tzinfo=utc)),
        ),
    ]
