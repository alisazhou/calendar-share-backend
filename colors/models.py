from django.db import models

from profiles.models import Profile
from calendars.models import Calendar


class Color(models.Model):
    hex_value = models.CharField(max_length=6, verbose_name='Color')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
