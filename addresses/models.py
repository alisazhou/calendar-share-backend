from django.conf import settings
from django.db import models


class Address(models.Model):
    street = models.CharField(
        blank=True, max_length=100, verbose_name='Street')
    city = models.CharField(
        blank=True, max_length=100, verbose_name='City')
    state = models.CharField(
        blank=True, max_length=100, verbose_name='State')
    zipcode = models.CharField(
        blank=True, max_length=20, verbose_name='Zipcode')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, verbose_name='Owner')

    class Meta:
        verbose_name_plural = 'addresses'

    def __str__(self):
        return '{}, {}, {} {}'.format(self.street, self.city, self.state, self.zipcode)
