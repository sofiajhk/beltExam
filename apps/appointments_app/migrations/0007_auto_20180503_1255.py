# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-03 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments_app', '0006_auto_20180503_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(),
        ),
    ]
