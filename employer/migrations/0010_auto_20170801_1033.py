# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-01 10:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0009_remove_employer_profession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='address',
            field=models.CharField(default='abcdef', max_length=500),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company_registration',
            field=models.CharField(default='ABC-1234', max_length=200),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company_type',
            field=models.CharField(choices=[('Government', 'Government'), ('Private', 'Private')], default='Private', max_length=200),
        ),
        migrations.AlterField(
            model_name='employer',
            name='country',
            field=models.CharField(choices=[('Indian', 'Indian'), ('Foreign', 'Foreign')], default='Indian', max_length=200),
        ),
        migrations.AlterField(
            model_name='employer',
            name='email',
            field=models.CharField(default='nursing.consultant.2017@gmail.com', max_length=200),
        ),
        migrations.AlterField(
            model_name='employer',
            name='phone',
            field=models.CharField(default='9810117638', max_length=200),
        ),
        migrations.AlterField(
            model_name='employer',
            name='sector',
            field=models.CharField(choices=[('Health', 'Health'), ('Construction', 'Construction'), ('IT', 'IT'), ('Shipping', 'Shipping')], default='Health', max_length=200),
        ),
        migrations.AlterField(
            model_name='employer',
            name='website',
            field=models.URLField(default='http://example.com'),
        ),
    ]
