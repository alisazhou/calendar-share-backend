from django.db import models


class Address(models.Model):
    street_address = models.CharField(max_length=100, verbose_name='Street address')
    city = models.CharField(max_length=100, verbose_name='City')
    state = models.CharField(max_length=100, verbose_name='State')
    zipcode = models.CharField(max_length=20, verbose_name='Zipcode')

    class Meta:
        verbose_name_plural = 'addresses'

    def __str__(self):
        return '{}, {}, {} {}'.format(self.street_address, self.city, self.state, self.zipcode)
