from django.conf import settings
from django.db import models


class Calendar(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='calendars_owned',
        on_delete=models.CASCADE,
        verbose_name='Created by')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='calendars_shared',
        through='memberships.Membership',
        verbose_name='Shared with')

    def __str__(self):
        return self.title
