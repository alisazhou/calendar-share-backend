from django.conf import settings
from django.db import models

from calendars.models import Calendar


class Membership(models.Model):
    color_hex = models.CharField(max_length=7, verbose_name='Color')
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Member')
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, verbose_name='Calendar')
