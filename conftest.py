import pytest


pytest_plugins = [
    'addresses.tests.address_plugins',
    'calendars.tests.calendar_plugins',
    'events.tests.event_plugins',
    'profiles.tests.profile_plugins']


@pytest.fixture
def normal_user1(django_user_model):
    # create a non-admin user
    user = django_user_model(username='user1')
    user.set_password('qwerty123')
    user.save()
    return user


@pytest.fixture
def normal_user2(django_user_model):
    # create a second non-admin user
    user = django_user_model(username='user2')
    user.set_password('qwerty123')
    user.save()
    return user
