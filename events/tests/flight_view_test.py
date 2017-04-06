import json

from common.test_helpers import get_user_token
from events.models import Flight
from events.tests.event_plugins import check_event_is_instance, get_response_non_field_errors


def test_get_flights_list(client, create_flights):
    # anon user gets 401
    response = client.get('/api/flights/')
    assert response.status_code == 401

    # login as normal_user1 gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/flights/', HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    # only sees autosaved membership of self
    flights_json = json.loads(response.content.decode())
    assert len(flights_json) == 1
    retrieved_flight = flights_json[0]
    flight_instance = Flight.objects.get(title=retrieved_flight['title'])
    # check username to see it is for normal_user1
    assert flight_instance.owner.username == 'user1'
    check_event_is_instance(retrieved_flight, flight_instance, serialized=True)

    # login as normal_user2 gets 200
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.get(
        '/api/flights/', HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    # only sees autosaved membership of self
    flights_json = json.loads(response.content.decode())
    assert len(flights_json) == 1
    retrieved_flight = flights_json[0]
    flight_instance = Flight.objects.get(title=retrieved_flight['title'])
    # check username to see it is for normal_user2
    assert flight_instance.owner.username == 'user2'
    check_event_is_instance(retrieved_flight, flight_instance, serialized=True)


def test_get_flight_by_id(client, create_flights):
    flight1 = Flight.objects.get(owner__username='user1')
    flight2 = Flight.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.get('/api/flights/{}/'.format(flight1.id))
    assert response.status_code == 401

    # login as normal_user1 gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/flights/{}/'.format(flight1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    # sees own flight
    flight_json1 = json.loads(response.content.decode())
    check_event_is_instance(flight_json1, flight1, serialized=True)
    # cannot see normal_user2's flight
    response = client.get(
        '/api/flights/{}/'.format(flight2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404

    # login as normal_user2 gets 200
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.get(
        '/api/flights/{}/'.format(flight2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    # sees own flight
    flight_json2 = json.loads(response.content.decode())
    check_event_is_instance(flight_json2, flight2, serialized=True)
    # cannot see normal_user1's flight
    response = client.get(
        '/api/flights/{}/'.format(flight1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 404


def test_post_flights(client, flight1_for_view, flight2_for_view):
    # anon user gets 401
    response = client.post('/api/flights/', flight1_for_view)
    assert response.status_code == 401

    # login as normal_user1, can create flight to own calendar
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.post(
        '/api/flights/', flight1_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 201
    assert Flight.objects.count() == 1
    # check normal_user1 is saved as owner
    flight1 = Flight.objects.get(title='flight 1')
    assert flight1.owner.username == 'user1'
    # cannot create flight to normal_user2's calendar
    response = client.post(
        '/api/flights/', flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 400    # cal2 is not part of queryset

    # login as normal_user2, can create flight to own calendar
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.post(
        '/api/flights/', flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 201
    assert Flight.objects.count() == 2
    # check normal_user2 is saved as owner
    flight2 = Flight.objects.get(title='flight 2')
    assert flight2.owner.username == 'user2'
    # cannot create flight to normal_user2's calendar
    response = client.post(
        '/api/flights/', flight1_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 400    # cal1 is not part of queryset


def test_delete_flights(client, create_flights):
    flight1 = Flight.objects.get(owner__username='user1')
    flight2 = Flight.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.delete('/api/flights/{}/'.format(flight1.id))
    assert response.status_code == 401
    assert Flight.objects.count() == 2

    # login as normal_user1, can delete own flight
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.delete(
        '/api/flights/{}/'.format(flight1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 204
    assert Flight.objects.count() == 1
    # cannot delete normal_user2's flight
    response = client.delete(
        '/api/flights/{}/'.format(flight2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404
    assert Flight.objects.count() == 1

    # login as normal_user2, can delete own flight
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.delete(
        '/api/flights/{}/'.format(flight2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 204
    assert Flight.objects.count() == 0


def test_patch_flights(client, create_flights):
    flight1 = Flight.objects.get(owner__username='user1')
    flight2 = Flight.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.patch(
        '/api/flights/{}/'.format(flight1.id),
        data=json.dumps({'title': 'new title'}),
        content_type='application/json')
    assert response.status_code == 401

    # login as normal_user1, can patch own flight
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.patch(
        '/api/flights/{}/'.format(flight1.id),
        data=json.dumps({'title': 'new title 1'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    # check only flight title has been updated
    flight1 = Flight.objects.get(owner__username='user1')
    assert flight1.title == 'new title 1'
    assert flight1.notes == 'notes on flight 1'
    # cannot patch normal_user2's flight
    response = client.patch(
        '/api/flights/{}/'.format(flight2.id),
        data=json.dumps({'title': 'new title from user1'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404
    flight1 = Flight.objects.get(owner__username='user1')
    assert flight1.title == 'new title 1'

    # login as normal_user2, can patch own flight
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.patch(
        '/api/flights/{}/'.format(flight2.id),
        data=json.dumps({'title': 'new title 2'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    # check only flight title has been updated
    flight2 = Flight.objects.get(owner__username='user2')
    assert flight2.title == 'new title 2'
    assert flight2.departure == 'SFO'
    # cannot patch normal_user1's flight
    response = client.patch(
        '/api/flights/{}/'.format(flight1.id),
        data=json.dumps({'title': 'new title from user2'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 404
    flight2 = Flight.objects.get(owner__username='user2')
    assert flight2.title == 'new title 2'


def test_start_cannot_be_after_end(client, flight2_for_view):
    # login as normal_user2
    user2_token = get_user_token(client, 'user2', 'qwerty123')

    # change flight2 start_at to be after end_at
    flight2_for_view['start_at'] = '2017-03-20 04:00'
    response = client.post(
        '/api/flights/', data=flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'End time must come after start.' in non_field_errors


def test_must_have_airline_and_flight_no_on_post_if_confirmed(client, flight2_for_view):
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    # change flight2 confirmed to True with no airline, results in error
    flight2_for_view['confirmed'] = True
    response = client.post(
        '/api/flights/', data=flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'Airline is required' in non_field_errors
    assert Flight.objects.count() == 0

    # add airline to confirmed_flight, results in error re flight_no
    flight2_for_view['airline'] = 'jetblue'
    response = client.post(
        '/api/flights/', data=flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'Flight number is required' in non_field_errors
    assert Flight.objects.count() == 0

    # add flight_no to confirmed_flight, no more errors
    flight2_for_view['flight_no'] = 1415
    response = client.post(
        '/api/flights/', data=flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 201
    assert Flight.objects.count() == 1


def test_must_have_airline_and_flight_no_on_patch_if_confirmed(
        client, flight1_for_view, flight2_for_view):
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    # create an unconfirmed flight1 with airline and flight_no
    flight1_for_view['confirmed'] = False
    client.post(
        '/api/flights/', data=flight1_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    flight1_id = Flight.objects.first().id

    # confirm flight1, no need for airline and flight_no (already exist)
    response1 = client.patch(
        '/api/flights/{}/'.format(flight1_id),
        data=json.dumps({'confirmed': True}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response1.status_code == 200

    # login as user2, create an unconfirmed flight2 with no airline or flight_no
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    client.post(
        '/api/flights/', data=flight2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    flight2_id = Flight.objects.get(title='flight 2').id

    # confirm flight2, need airline and flight_no
    flight2_for_view['confirmed'] = True
    response2 = client.patch(
        '/api/flights/{}/'.format(flight2_id),
        data=json.dumps(flight2_for_view),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 400
    non_field_errors = get_response_non_field_errors(response2)
    assert 'Airline is required' in non_field_errors

    flight2_for_view['airline'] = 'jetblue'
    response2 = client.patch(
        '/api/flights/{}/'.format(flight2_id),
        data=json.dumps(flight2_for_view),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 400
    non_field_errors = get_response_non_field_errors(response2)
    assert 'Flight number is required' in non_field_errors

    flight2_for_view['flight_no'] = 1415
    response2 = client.patch(
        '/api/flights/{}/'.format(flight2_id),
        data=json.dumps(flight2_for_view),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 200
