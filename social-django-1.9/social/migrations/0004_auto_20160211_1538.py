# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20160210_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='following',
        ),
        migrations.AddField(
            model_name='member',
            name='friends',
            field=models.ManyToManyField(related_name='_member_friends_+', to='social.Member'),
        ),
    ]
