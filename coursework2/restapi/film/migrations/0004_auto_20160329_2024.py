# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-29 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0003_auto_20160329_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='actors',
            field=models.ManyToManyField(null=True, to='film.Actor'),
        ),
    ]
