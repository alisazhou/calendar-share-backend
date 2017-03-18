import pytest

from addresses.models import Address


@pytest.fixture
def address1():
    street = '1 Main Street Apt 1'
    city = 'Brooklyn'
    state = 'NY'
    zipcode = '11215'
    address = {'street': street, 'city': city, 'state': state, 'zipcode': zipcode}
    return address


@pytest.fixture
def address2():
    street = '2 Main Street Apt 2'
    city = 'San Francisco'
    state = 'CA'
    zipcode = '94102'
    address = {'street': street, 'city': city, 'state': state, 'zipcode': zipcode}
    return address


@pytest.fixture
def create_addresses(address1, address2, db):
    Address.objects.create(
        street=address1['street'],
        city=address1['city'],
        state=address1['state'],
        zipcode=address1['zipcode'])
    Address.objects.create(
        street=address2['street'],
        city=address2['city'],
        state=address2['state'],
        zipcode=address2['zipcode'])
