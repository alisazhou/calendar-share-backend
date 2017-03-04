from django.conf import settings
from django.db import models

from calendars.models import Calendar


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='Created by')
    calendar = models.ForeignKey(
        Calendar,
        on_delete=models.CASCADE,
        verbose_name='Calendar')
    start_at = models.DateTimeField(verbose_name='Start')
    end_at = models.DateTimeField(verbose_name='End')
    confirmed = models.BooleanField(verbose_name='Confirmed?')
    location = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Location')
    notes = models.TextField(blank=True, verbose_name='Notes')
