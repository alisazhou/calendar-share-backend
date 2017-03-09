# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 02:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('calendars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_hex', models.CharField(max_length=6, verbose_name='Color')),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendars.Calendar', verbose_name='Calendar')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile', verbose_name='Member')),
            ],
        ),
    ]
