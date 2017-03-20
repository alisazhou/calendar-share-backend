from django.conf import settings
from django.db import models

from calendars.models import Calendar


class AbstractEvent(models.Model):
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
    notes = models.TextField(blank=True, verbose_name='Notes')

    class Meta:
        abstract = True
        ordering = ['-start_at', ]


class Flight(AbstractEvent):
    departure = models.CharField(max_length=20, verbose_name='Departure airport')
    arrival = models.CharField(max_length=20, verbose_name='Arrival airport')
    airline = models.CharField(max_length=20, blank=True, null=True, verbose_name='Airline')
    flight_no = models.IntegerField(blank=True, null=True, verbose_name='Flight number')

    def __str__(self):
        return '{title} from {departure} to {arrival}'.format(
            title=self.title, departure=self.departure, arrival=self.arrival)


class Plan(AbstractEvent):
    location = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Location')

    def __str__(self):
        return self.title
