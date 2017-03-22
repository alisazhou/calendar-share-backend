import json

from events.models import Plan
from events.tests.event_plugins import check_event_is_instance, get_response_non_field_errors


def test_get_plans_list(client, create_plans):
    response = client.get('/api/plans/')
    assert response.status_code == 200

    plans_json = json.loads(response.content.decode())
    assert len(plans_json) == 2

    for plan_dict in plans_json:
        plan_title = plan_dict['title']
        plan_instance = Plan.objects.get(title=plan_title)
        check_event_is_instance(plan_dict, plan_instance, serialized=True)


def test_get_plan_by_id(client, create_plans):
    plan1, plan2 = Plan.objects.all()

    response1 = client.get('/api/plans/{}/'.format(plan1.id))
    assert response1.status_code == 200
    plan1_json = json.loads(response1.content.decode())
    check_event_is_instance(plan1_json, plan1, serialized=True)

    response2 = client.get('/api/plans/{}/'.format(plan2.id))
    assert response2.status_code == 200
    plan2_json = json.loads(response2.content.decode())
    check_event_is_instance(plan2_json, plan2, serialized=True)


def test_post_plans(admin_client, plan1_for_view, plan2_for_view):
    response1 = admin_client.post('/api/plans/', plan1_for_view)
    assert response1.status_code == 201
    assert Plan.objects.count() == 1

    response2 = admin_client.post('/api/plans/', plan2_for_view)
    assert response2.status_code == 201
    assert Plan.objects.count() == 2


def test_delete_plans(client, create_plans):
    plan1, plan2 = Plan.objects.all()

    client.delete('/api/plans/{}/'.format(plan1.id))
    assert Plan.objects.count() == 1

    client.delete('/api/plans/{}/'.format(plan2.id))
    assert Plan.objects.count() == 0


def test_patch_plans(client, create_plans):
    plan1 = Plan.objects.first()
    orig_title = plan1.title
    orig_owner = plan1.owner

    response = client.patch(
        '/api/plans/{}/'.format(plan1.id),
        data=json.dumps({'title': 'new title'}),
        content_type='application/json')
    assert response.status_code == 200

    plan1 = Plan.objects.first()
    assert plan1.title != orig_title
    assert plan1.owner == orig_owner


def test_start_cannot_be_after_end(client, plan2_for_view):
    # change plan1 start_at to be after end_at
    plan2_for_view['start_at'] = '2017-04-20 04:00'
    response = client.post('/api/plans/', data=plan2_for_view)
    assert response.status_code == 400
    non_field_errors = get_response_non_field_errors(response)
    assert 'End time must come after start.' in non_field_errors
