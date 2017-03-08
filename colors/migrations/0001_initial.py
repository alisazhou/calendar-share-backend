# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 20:42
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
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hex_value', models.CharField(max_length=6, verbose_name='Color')),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendars.Calendar')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
            ],
        ),
    ]
