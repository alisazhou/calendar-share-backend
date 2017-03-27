from django.conf import settings
from django.db import models


class Profile(models.Model):
    bday = models.DateField(blank=True, null=True, verbose_name='Birthday')
    phone = models.CharField(
        blank=True, max_length=20, null=True, unique=True, verbose_name='Phone number')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
