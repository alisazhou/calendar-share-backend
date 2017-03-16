import pytest

from addresses.models import Address



@pytest.fixture
def correct_address1():
    street = '1 Main Street Apt 1'
    city = 'Brooklyn'
    state = 'NY'
    zipcode = '11215'
    address = {'street': street, 'city': city, 'state': state, 'zipcode': zipcode}
    return address

@pytest.fixture
def correct_address2():
    street = '2 Main Street Apt 2'
    city = 'San Francisco'
    state = 'CA'
    zipcode = '94102'
    address = {'street': street, 'city': city, 'state': state, 'zipcode': zipcode}
    return address


@pytest.fixture
def create_addresses(correct_address1, correct_address2, db):
    address1 = Address.objects.create(
        street=correct_address1['street'],
        city=correct_address1['city'],
        state=correct_address1['state'],
        zipcode=correct_address1['zipcode'])
    address2 = Address.objects.create(
        street=correct_address2['street'],
        city=correct_address2['city'],
        state=correct_address2['state'],
        zipcode=correct_address2['zipcode'])


