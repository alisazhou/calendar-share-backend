from django.contrib.auth.models import User
from django.db import models

from addresses.models import Address


class Profile(models.Model):
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name='Address')
    bday = models.DateField(verbose_name='Birthday')
    phone = models.CharField(
        blank=True,
        max_length=20,
        unique=True,
        verbose_name='Phone number')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
