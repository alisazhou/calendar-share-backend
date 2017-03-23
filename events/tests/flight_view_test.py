import json

from events.models import Flight
from events.tests.event_plugins import check_event_is_instance, get_response_non_field_errors


def test_get_flights_list(client, create_flights):
    response = client.get('/api/flights/')
    assert response.status_code == 200

    flights_json = json.loads(response.content.decode())
    assert len(flights_json) == 2

    for flight_dict in flights_json:
        flight_title = flight_dict['title']
        flight_instance = Flight.objects.get(title=flight_title)
        check_event_is_instance(flight_dict, flight_instance, serialized=True)


def test_get_flight_by_id(client, create_flights):
    flight1, flight2 = Flight.objects.all()

    response1 = client.get('/api/flights/{}/'.format(flight1.id))
    assert response1.status_code == 200
    flight_json1 = json.loads(response1.content.decode())
    check_event_is_instance(flight_json1, flight1, serialized=True)

    response2 = client.get('/api/flights/{}/'.format(flight2.id))
    assert response2.status_code == 200
    flight_json2 = json.loads(response2.content.decode())
    check_event_is_instance(flight_json2, flight2, serialized=True)


def test_post_flights(client, flight1_for_view, flight2_for_view, create_profiles):
    client.login(username='user1', password='qwerty123')
    response1 = client.post('/api/flights/', flight1_for_view)
    assert response1.status_code == 201
    assert Flight.objects.count() == 1
    # check normal_user1 is saved as owner
    flight1 = Flight.objects.get(title='flight 1')
    assert flight1.owner.username == 'user1'

    client.logout()
    client.login(username='user2', password='qwerty123')
    response2 = client.post('/api/flights/', flight2_for_view)
    assert response2.status_code == 201
    assert Flight.objects.count() == 2
    # check normal_user2 is saved as owner
    flight2 = Flight.objects.get(title='flight 2')
    assert flight2.owner.username == 'user2'


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


def test_start_cannot_be_after_end(client, flight2_for_view):
    # change flight2 start_at to be after end_at
    flight2_for_view['start_at'] = '2017-03-20 04:00'
    response = client.post('/api/flights/', data=flight2_for_view)
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'End time must come after start.' in non_field_errors


def test_must_have_airline_and_flight_no_on_post_if_confirmed(client, flight2_for_view):
    client.login(username='user2', password='qwerty123')
    # change flight2 confirmed to True with no airline, results in error
    flight2_for_view['confirmed'] = True
    response = client.post('/api/flights/', data=flight2_for_view)
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'Airline is required' in non_field_errors
    assert Flight.objects.count() == 0

    # add airline to confirmed_flight, results in error re flight_no
    flight2_for_view['airline'] = 'jetblue'
    response = client.post('/api/flights/', data=flight2_for_view)
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'Flight number is required' in non_field_errors
    assert Flight.objects.count() == 0

    # add flight_no to confirmed_flight, no more errors
    flight2_for_view['flight_no'] = 1415
    response = client.post('/api/flights/', data=flight2_for_view)
    assert response.status_code == 201
    assert Flight.objects.count() == 1


def test_must_have_airline_and_flight_no_on_patch_if_confirmed(
        client, flight1_for_view, flight2_for_view):
    client.login(username='user1', password='qwerty123')
    # create an unconfirmed flight1 with airline and flight_no
    flight1_for_view['confirmed'] = False
    client.post('/api/flights/', data=flight1_for_view)
    flight1_id = Flight.objects.first().id

    # confirm flight1, no need for airline and flight_no
    response1 = client.patch(
        '/api/flights/{}/'.format(flight1_id),
        data=json.dumps({'confirmed': True}),
        content_type='application/json')
    assert response1.status_code == 200

    # create an unconfirmed flight2 with no airline and flight_no
    client.post('/api/flights/', data=flight2_for_view)
    flight2_id = Flight.objects.get(title='flight 2').id

    # confirm flight2, need airline and flight_no
    flight2_for_view['confirmed'] = True
    response2 = client.patch(
        '/api/flights/{}/'.format(flight2_id),
        data=json.dumps(flight2_for_view),
        content_type='application/json')
    assert response2.status_code == 400
    non_field_errors = get_response_non_field_errors(response2)
    assert 'Airline is required' in non_field_errors

    flight2_for_view['airline'] = 'jetblue'
    response2 = client.patch(
        '/api/flights/{}/'.format(flight2_id),
        data=json.dumps(flight2_for_view),
        content_type='application/json')
    assert response2.status_code == 400
    non_field_errors = get_response_non_field_errors(response2)
    assert 'Flight number is required' in non_field_errors

    flight2_for_view['flight_no'] = 1415
    response2 = client.patch(
        '/api/flights/{}/'.format(flight2_id),
        data=json.dumps(flight2_for_view),
        content_type='application/json')
    assert response2.status_code == 200
