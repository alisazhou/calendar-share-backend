import pytest

from calendars.models import Calendar
from events.models import Flight


def check_date_time_object_and_str_are_the_same(dt_obj, dt_str):
    assert '{:%Y-%m-%d}'.format(dt_obj) in dt_str
    assert '{:%H:%M}'.format(dt_obj) in dt_str


@pytest.fixture
def flight1(normal_user1, create_calendars):
    cal1 = Calendar.objects.first()
    flight_info = {
        'title': 'flight 1', 'owner': normal_user1, 'calendar': cal1,
        'start_at': '2017-03-17 01:00', 'end_at': '2017-03-18 02:00',
        'confirmed': True, 'notes': 'notes on flight 1',
        'departure': 'JFK', 'arrival': 'SFO', 'airline': 'virgin',
        'flight_no': 1}
    return flight_info


@pytest.fixture
def flight1_for_view(flight1):
    flight_info = flight1.copy()
    flight_info.pop('owner')
    flight_info['calendar'] = '/api/calendars/{}/'.format(flight1['calendar'].id)
    return flight_info


@pytest.fixture
def flight2(normal_user2, create_calendars):
    # flight 2 only has required fields filled out
    cal2 = Calendar.objects.all()[1]
    flight_info = {
        'title': 'flight 2', 'owner': normal_user2, 'calendar': cal2,
        'start_at': '2017-03-19 02:00', 'end_at': '2017-03-20 03:00',
        'confirmed': False, 'departure': 'SFO', 'arrival': 'JFK'}
    return flight_info


@pytest.fixture
def flight2_for_view(flight2):
    flight_info = flight2.copy()
    flight_info.pop('owner')
    flight_info['calendar'] = '/api/calendars/{}/'.format(flight2['calendar'].id)
    return flight_info


@pytest.fixture
def create_flights(flight1, flight2):
    flight_instance1 = Flight()
    for k, v in flight1.items():
        setattr(flight_instance1, k, v)
    flight_instance1.save()

    flight_instance2 = Flight()
    for k, v in flight2.items():
        setattr(flight_instance2, k, v)
    flight_instance2.save()