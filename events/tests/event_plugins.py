import json
import pytest

from calendars.models import Calendar
from events.models import Flight, Plan


def check_date_time_object_and_str_are_the_same(dt_obj, dt_str):
    assert '{:%Y-%m-%d}'.format(dt_obj) in dt_str
    assert '{:%H:%M}'.format(dt_obj) in dt_str


def check_evt_owner_instance_corresponds_to_serialized_url(evt_ins, url):
    owner_id = evt_ins.owner.id
    assert '/api/profiles/{}/'.format(owner_id) in url


def check_evt_calendar_instance_corresponds_to_serialized_url(evt_ins, url):
    calendar_id = evt_ins.calendar.id
    assert '/api/calendars/{}/'.format(calendar_id) in url


def get_response_non_field_errors(response):
    errs = json.loads(response.content.decode())
    non_field_errors = errs.get('non_field_errors')
    return non_field_errors


def check_event_is_instance(evt_dict, evt_ins, serialized=False):
    # check start and end times are the same
    start_at = evt_dict.pop('start_at')
    check_date_time_object_and_str_are_the_same(evt_ins.start_at, start_at)
    end_at = evt_dict.pop('end_at')
    check_date_time_object_and_str_are_the_same(evt_ins.end_at, end_at)

    # if evt_dict is the serialized json, not the fixture dict, FK and MTM
    # are serialized as urls
    if serialized:
        owner_url = evt_dict.pop('owner')
        check_evt_owner_instance_corresponds_to_serialized_url(evt_ins, owner_url)
        cal_url = evt_dict.pop('calendar')
        check_evt_calendar_instance_corresponds_to_serialized_url(evt_ins, cal_url)
        # pop the superfluous url field that is just flight id
        evt_dict.pop('url')

    # check the rest of the fields
    for k, v in evt_dict.items():
        assert getattr(evt_ins, k) == v


@pytest.fixture
def flight1(normal_user1, create_calendars):
    cal1 = Calendar.objects.get(owner=normal_user1)
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
    cal2 = Calendar.objects.get(owner=normal_user2)
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


@pytest.fixture
def plan1(normal_user1, create_calendars):
    cal1 = Calendar.objects.first()
    plan_info = {
        'title': 'plan 1', 'owner': normal_user1, 'calendar': cal1,
        'start_at': '2017-04-17 01:00', 'end_at': '2017-04-18 02:00',
        'confirmed': True, 'notes': 'notes on plan 1', 'location': 'alamo'}
    return plan_info


@pytest.fixture
def plan1_for_view(plan1):
    owner_id = plan1['owner'].id
    plan1['owner'] = '/api/profiles/{}/'.format(owner_id)
    cal1_id = plan1['calendar'].id
    plan1['calendar'] = '/api/calendars/{}/'.format(cal1_id)
    return plan1


@pytest.fixture
def plan2(normal_user2, create_calendars):
    cal2 = Calendar.objects.first()
    plan_info = {
        'title': 'plan 2', 'owner': normal_user2, 'calendar': cal2,
        'start_at': '2017-04-19 02:00', 'end_at': '2017-04-20 03:00',
        'confirmed': False}
    return plan_info


@pytest.fixture
def plan2_for_view(plan2):
    owner_id = plan2['owner'].id
    plan2['owner'] = '/api/profiles/{}/'.format(owner_id)
    cal2_id = plan2['calendar'].id
    plan2['calendar'] = '/api/calendars/{}/'.format(cal2_id)
    return plan2


@pytest.fixture
def create_plans(plan1, plan2):
    plan_instance2 = Plan()
    for k, v in plan2.items():
        setattr(plan_instance2, k, v)
    plan_instance2.save()

    plan_instance1 = Plan()
    for k, v in plan1.items():
        setattr(plan_instance1, k, v)
    plan_instance1.save()
