# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-30 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0005_auto_20160330_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='actors',
            field=models.ManyToManyField(blank=True, to='film.Actor'),
        ),
    ]
