import pytest


pytest_plugins = [
    'addresses.tests.address_plugins',
    'calendars.tests.calendar_plugins',
    'memberships.tests.membership_plugins',
    'profiles.tests.profile_plugins']


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
