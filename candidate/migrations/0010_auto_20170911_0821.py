# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-11 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0009_auto_20170910_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eligibilitytests',
            name='eligibility_tests',
            field=models.CharField(blank=True, choices=[('Prometric (Specify country)', 'Prometric (Specify country)'), ('HAAD', 'HAAD'), ('DHA', 'DHA'), ('IELTS', 'IELTS'), ('CGFNS', 'CGFNS'), ('TOEFL', 'TOEFL'), ('OET', 'OET'), ('Other', 'Other')], max_length=50),
        ),
    ]
