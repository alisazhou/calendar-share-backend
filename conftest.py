import pytest

from calendars.models import Calendar
from memberships.models import Membership
from profiles.models import Profile


pytest_plugins = [
    'addresses.tests.address_plugins',
    'calendars.tests.calendar_plugins',
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


@pytest.fixture
def create_memberships(create_calendars, create_profiles):
    # add incomplete_profile as member to calendar1
    profile2 = Profile.objects.all()[1]
    calendar1 = Calendar.objects.first()
    Membership.objects.create(
        color_hex='000000', member=profile2, calendar=calendar1)

    # add complete_profile as member to calnedar2
    profile1 = Profile.objects.first()
    calendar2 = Calendar.objects.all()[1]
    Membership.objects.create(
        color_hex='FFFFFF', member=profile1, calendar=calendar2)
