from django.contrib.auth.models import User
from django.db import models


class Calendar(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    owner = models.ForeignKey(
        User, related_name='calendars_owned', on_delete=models.CASCADE,
        verbose_name='Created by')
    members = models.ManyToManyField(
        User, related_name='calendars_shared', verbose_name='Shared with')
