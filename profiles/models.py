from django.contrib.auth.models import User
from django.db import models

from addresses.models import Address


class Profile(models.Model):
    address = models.OneToOneField(
        Address,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Address')
    bday = models.DateField(blank=True, verbose_name='Birthday')
    phone = models.CharField(
        blank=True,
        max_length=20,
        unique=True,
        verbose_name='Phone number')
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
