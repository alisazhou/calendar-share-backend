import pytest

from profiles.models import Profile


@pytest.fixture
def complete_profile(create_addresses, normal_user1):
    profile_info = {
        'bday': '2017-03-17', 'phone': '9171234567', 'user': normal_user1}
    return profile_info


@pytest.fixture
def complete_profile_for_view():
    profile_info = {
        'bday': '2017-03-18', 'phone': '2121234567', 'username': 'user3',
        'password': 'qwerty123', 'email': 'user3@test.com',
        'first_name': 'first3', 'last_name': 'last3'}
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
        bday=complete_profile['bday'],
        phone=complete_profile['phone'],
        user=complete_profile['user'])
    # Create incomplete profile with only required user field filled out
    Profile.objects.create(user=incomplete_profile['user'])
