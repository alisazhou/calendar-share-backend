pytest_plugins = [
    'addresses.tests.address_plugins',
    'profiles.tests.profile_plugins']

import pytest



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
