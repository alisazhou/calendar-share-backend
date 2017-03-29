import pytest

from calendars.models import Calendar
from memberships.models import Membership


@pytest.fixture
def calendar1(normal_user1):
    calendar_info = {
        'title': 'calendar 1',
        'owner': normal_user1}
    return calendar_info


@pytest.fixture
def calendar2(normal_user2):
    calendar_info = {
        'title': 'calendar 2',
        'owner': normal_user2}
    return calendar_info


@pytest.fixture
def create_calendars(calendar1, calendar2, normal_user1, normal_user2):
    # members is a 'through' field, and is created via Membership instances
    cal1 = Calendar.objects.create(
        title=calendar1['title'],
        owner=calendar1['owner'])
    # imitate view behavior of autosaving self membership
    Membership.objects.create(
        color_hex='111111', calendar=cal1, member=normal_user1)
    cal2 = Calendar.objects.create(
        title=calendar2['title'],
        owner=calendar2['owner'])
    # imitate view behavior of autosaving self membership
    Membership.objects.create(
        color_hex='222222', calendar=cal2, member=normal_user2)
