from django.db import models

from calendars.models import Calendar
from profiles.models import Profile


class Membership(models.Model):
    color_hex = models.CharField(max_length=6, verbose_name='Color')
    member = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name='Member')
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, verbose_name='Calendar')
