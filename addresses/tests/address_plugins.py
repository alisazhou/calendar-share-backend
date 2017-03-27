import pytest

from addresses.models import Address


def check_address_is_instance(address_dict, address_instance):
    user = address_dict.pop('user')
    if type(user) == str:
        # if json from response, then user is serialized as the id
        assert '/api/profiles/{}/'.format(address_instance.user.id) in user
    else:
        # if comparing to fixture, user is django user instance
        assert address_instance.user == user

    # url is a serialized field, no need to check
    address_dict.pop('url', '')

    for k, v in address_dict.items():
        assert getattr(address_instance, k) == v


@pytest.fixture
def address1(normal_user1):
    address = {
        'street': '1 Main Street Apt 1',
        'city': 'Brooklyn',
        'state': 'NY',
        'zipcode': '11215',
        'user': normal_user1}
    return address


@pytest.fixture
def address2(normal_user2):
    address = {
        'street': '2 Main Street Apt 2',
        'city': 'San Francisco',
        'state': 'CA',
        'zipcode': '94102',
        'user': normal_user2}
    return address


@pytest.fixture
def create_addresses(address1, address2):
    address_ins1 = Address()
    for k, v in address1.items():
        setattr(address_ins1, k, v)
    address_ins1.save()

    address_ins2 = Address()
    for k, v in address2.items():
        setattr(address_ins2, k, v)
    address_ins2.save()
