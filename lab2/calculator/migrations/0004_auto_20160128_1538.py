# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_auto_20160128_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saving',
            name='years',
            field=models.IntegerField(default=5),
        ),
    ]
