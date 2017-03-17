import pytest

from addresses.models import Address
from profiles.models import Profile



@pytest.fixture
def normal_user1(django_user_model):
    # create a non-admin user
    user = django_user_model.objects.create(username='user1', password='qwerty123')
    return user

@pytest.fixture
def normal_user2(django_user_model):
    # create a second non-admin user
    user = django_user_model.objects.create(username='user2', password='qwerty123')
    return user



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



@pytest.fixture
def complete_profile(create_addresses, normal_user1):
    address = Address.objects.all()[0]
    bday = '2017-03-17'
    phone = '9171234567'
    profile_info = {
        'address': address, 'bday': bday, 'phone': phone, 'user': normal_user1}
    return profile_info

@pytest.fixture
def complete_profile_for_view():
    profile_info = {
        'street': '3 Main St Apt 3',
        'city': 'New York',
        'state': 'NY',
        'zipcode': '10128',
        'bday': '2017-03-18',
        'phone': '2121234567',
        'username': 'user3',
        'password': 'qwerty123',
        'email': 'user3@test.com',
        'first_name': 'first3',
        'last_name': 'last3'}
    return profile_info

@pytest.fixture
def incomplete_profile(normal_user2):
    profile_info = {'user': normal_user2}
    return profile_info

@pytest.fixture
def incomplete_profile_for_view():
    profile_info = {
        'username': 'user4',
        'password': 'qwerty123',
        'email': 'user4@test.com',
        'first_name': 'first4',
        'last_name': 'last4'}
    return profile_info


@pytest.fixture
def create_profiles(complete_profile, incomplete_profile):
    # Create complete profile with all fields filled out
    Profile.objects.create(
        address=complete_profile['address'],
        bday=complete_profile['bday'],
        phone=complete_profile['phone'],
        user=complete_profile['user'])
    # Create incomplete profile with only required user field filled out
    Profile.objects.create(user=incomplete_profile['user'])
