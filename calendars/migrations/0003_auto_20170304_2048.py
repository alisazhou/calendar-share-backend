# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 20:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_auto_20170304_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='members',
            field=models.ManyToManyField(related_name='calendars_shared', to=settings.AUTH_USER_MODEL, verbose_name='Shared with'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendars_owned', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
    ]
