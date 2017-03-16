import pytest

from addresses.models import Address
from profiles.models import Profile



@pytest.fixture
def normal_user1(django_user_model):
    # create a non-admin user
    user = django_user_model.objects.create(
        username='user1', password='qwerty123')
    return user

@pytest.fixture
def normal_user2(django_user_model):
    # create a second non-admin user
    user = django_user_model.objects.create(
        username='user2', password='qwerty123')
    return user



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
    Address.objects.create(
        street=correct_address1['street'],
        city=correct_address1['city'],
        state=correct_address1['state'],
        zipcode=correct_address1['zipcode'])
    Address.objects.create(
        street=correct_address2['street'],
        city=correct_address2['city'],
        state=correct_address2['state'],
        zipcode=correct_address2['zipcode'])



@pytest.fixture
def correct_complete_profile(create_addresses, normal_user1):
    address = Address.objects.all()[0]
    bday = '2017-03-17'
    phone = '9171234567'
    profile_info = {
        'address': address, 'bday': bday, 'phone': phone, 'user': normal_user1}
    return profile_info

@pytest.fixture
def correct_incomplete_profile(normal_user2):
    profile_info = {'user': normal_user2}
    return profile_info


@pytest.fixture
def create_profiles(correct_complete_profile, correct_incomplete_profile):
    # Create complete profile with all fields filled out
    Profile.objects.create(
        address=correct_complete_profile['address'],
        bday=correct_complete_profile['bday'],
        phone=correct_complete_profile['phone'],
        user=correct_complete_profile['user'])
    # Create incomplete profile with only required user field filled out
    Profile.objects.create(user=correct_incomplete_profile['user'])
