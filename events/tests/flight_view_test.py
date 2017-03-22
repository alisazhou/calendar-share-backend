import json

from events.models import Flight
from events.tests.event_plugins import check_date_time_object_and_str_are_the_same


def check_flight_is_instance(flight_dict, flight_instance):
    # check owner is the same as the serialized profile url
    owner_url = flight_dict.pop('owner')
    assert '/api/profiles/{}/'.format(flight_instance.owner.id) in owner_url

    # check calendar is the same as the serialized calendar url
    cal_url = flight_dict.pop('calendar')
    assert '/api/calendars/{}/'.format(flight_instance.calendar.id) in cal_url

    # check start and end times are the same as the serialized strings
    start_at = flight_dict.pop('start_at')
    check_date_time_object_and_str_are_the_same(flight_instance.start_at, start_at)
    end_at = flight_dict.pop('end_at')
    check_date_time_object_and_str_are_the_same(flight_instance.end_at, end_at)

    for k, v in flight_dict.items():
        assert getattr(flight_instance, k) == v


def test_get_flights_list(client, create_flights):
    response = client.get('/api/flights/')
    assert response.status_code == 200

    flights_json = json.loads(response.content.decode())
    assert len(flights_json) == 2

    for flight_dict in flights_json:
        flight_title = flight_dict['title']
        flight_instance = Flight.objects.get(title=flight_title)
        check_flight_is_instance(flight_dict, flight_instance)


def test_get_flight_by_id(client, create_flights):
    flight1, flight2 = Flight.objects.all()

    response1 = client.get('/api/flights/{}/'.format(flight1.id))
    assert response1.status_code == 200
    flight_json1 = json.loads(response1.content.decode())
    check_flight_is_instance(flight_json1, flight1)

    response2 = client.get('/api/flights/{}/'.format(flight2.id))
    assert response2.status_code == 200
    flight_json2 = json.loads(response2.content.decode())
    check_flight_is_instance(flight_json2, flight2)


def test_post_flights(admin_client, flight1_for_view, flight2_for_view):
    response1 = admin_client.post('/api/flights/', flight1_for_view)
    assert response1.status_code == 201
    assert Flight.objects.count() == 1

    response2 = admin_client.post('/api/flights/', flight2_for_view)
    assert response2.status_code == 201
    assert Flight.objects.count() == 2


def test_delete_flights(client, create_flights):
    flight1, flight2 = Flight.objects.all()

    client.delete('/api/flights/{}/'.format(flight1.id))
    assert Flight.objects.count() == 1

    client.delete('/api/flights/{}/'.format(flight2.id))
    assert Flight.objects.count() == 0


def test_patch_flights(client, create_flights):
    flight1 = Flight.objects.first()
    orig_title = flight1.title
    orig_owner = flight1.owner

    response = client.patch(
        '/api/flights/{}/'.format(flight1.id),
        data=json.dumps({'title': 'new title'}),
        content_type='application/json')
    assert response.status_code == 200

    flight1 = Flight.objects.first()
    # check title has been updated
    assert flight1.title != orig_title
    # check title has not changed
    assert flight1.owner == orig_owner
