import json

from common.test_helpers import get_user_token
from events.models import Plan
from events.tests.event_plugins import check_event_is_instance, get_response_non_field_errors


def test_get_plans_list(client, create_plans):
    # anon user gets 401
    response = client.get('/api/plans/')
    assert response.status_code == 401

    # login as user1, gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/plans/', HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    # sees calendar1 with autosaved membership
    plans_json = json.loads(response.content.decode())
    assert len(plans_json) == 1

    plan1 = Plan.objects.get(owner__username='user1')
    check_event_is_instance(plans_json[0], plan1, serialized=True)


def test_get_plan_by_id(client, create_plans):
    plan1 = Plan.objects.get(owner__username='user1')
    plan2 = Plan.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.get('/api/plans/{}/'.format(plan1.id))
    assert response.status_code == 401

    # login as user1, gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response1 = client.get(
        '/api/plans/{}/'.format(plan1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response1.status_code == 200
    plan1_json = json.loads(response1.content.decode())
    check_event_is_instance(plan1_json, plan1, serialized=True)
    # cannot get user2's plan
    response2 = client.get(
        '/api/plans/{}/'.format(plan2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 401

    # login as user2 gets 200
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response2 = client.get(
        '/api/plans/{}/'.format(plan2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 200
    plan2_json = json.loads(response2.content.decode())
    check_event_is_instance(plan2_json, plan2, serialized=True)
    # cannot get user2's plan
    response2 = client.get(
        '/api/plans/{}/'.format(plan1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 401


def test_post_plans(client, plan1_for_view, plan2_for_view):
    # anon user gets 401, nothing posted
    response = client.post('/api/plans/', plan1_for_view)
    assert response.status_code == 401
    assert Plan.objects.count() == 0

    # login as user1 gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response1 = client.post(
        '/api/plans/', plan1_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response1.status_code == 201
    assert Plan.objects.count() == 1
    # check plan1's owner is normal_user1
    plan1 = Plan.objects.get(title='plan 1')
    assert plan1.owner.username == 'user1'

    # login as user2 gets 200
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response2 = client.post(
        '/api/plans/', plan2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 201
    assert Plan.objects.count() == 2
    # check plan2's owner is normal_user2
    plan2 = Plan.objects.get(title='plan 2')
    assert plan2.owner.username == 'user2'


def test_delete_plans(client, create_plans):
    plan1 = Plan.objects.get(owner__username='user1')
    plan2 = Plan.objects.get(owner__username='user2')

    # anon user gets 401, nothing deleted
    response = client.delete('/api/plans/{}/'.format(plan1.id))
    assert response.status_code == 401
    assert Plan.objects.count() == 2

    # login as normal_user1, can delete own plan
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.delete(
        '/api/plans/{}/'.format(plan1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 204
    assert Plan.objects.count() == 1
    # cannot delete user2's plan
    response = client.delete(
        '/api/plans/{}/'.format(plan2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404

    # login as normal_user2, can delete own plan
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.delete(
        '/api/plans/{}/'.format(plan2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 204
    assert Plan.objects.count() == 0


def test_patch_plans(client, create_plans):
    plan1 = Plan.objects.get(owner__username='user1')

    # anon user gets 401
    response = client.patch(
        '/api/plans/{}/'.format(plan1.id),
        data=json.dumps({'title': 'new title'}),
        content_type='application/json')
    assert response.status_code == 401

    # login as normal_user1, gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.patch(
        '/api/plans/{}/'.format(plan1.id),
        data=json.dumps({'title': 'new title for plan 1'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200

    plan1 = Plan.objects.get(owner__username='user1')
    # check title has changed, but not other fields
    assert plan1.title == 'new title for plan 1'
    assert plan1.notes == 'notes on plan 1'


def test_start_cannot_be_after_end(client, plan2_for_view):
    # change plan2 start_at to be after end_at
    plan2_for_view['start_at'] = '2017-04-20 04:00'

    # login as normal_user2
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.post(
        '/api/plans/', data=plan2_for_view,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'End time must come after start.' in non_field_errors
