# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 21:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bday', models.DateField(verbose_name='Birthday')),
                ('phone', models.CharField(blank=True, max_length=20, unique=True, verbose_name='Phone number')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='addresses.Address', verbose_name='Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
