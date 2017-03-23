import pytest

from calendars.models import Calendar
from memberships.models import Membership


@pytest.fixture
def create_memberships(normal_user1, normal_user2, create_calendars):
    # add normal_user2 as member to calendar1
    calendar1 = Calendar.objects.first()
    Membership.objects.create(
        color_hex='000000', member=normal_user2, calendar=calendar1)

    # add normal_user1 as member to calendar2
    calendar2 = Calendar.objects.all()[1]
    Membership.objects.create(
        color_hex='FFFFFF', member=normal_user1, calendar=calendar2)
