import pytest

from calendars.models import Calendar



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
def create_calendars(calendar1, calendar2):
    # members is a 'through' field, and is created via Membership instances
    Calendar.objects.create(
        title=calendar1['title'],
        owner=calendar1['owner'])
    Calendar.objects.create(
        title=calendar2['title'],
        owner=calendar2['owner'])
