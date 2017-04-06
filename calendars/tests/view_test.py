import json
import re

from calendars.models import Calendar
from common.test_helpers import get_user_token
from memberships.models import Membership


def check_calendar_is_instance(cal_dict, cal_instance):
    assert cal_dict['title'] == cal_instance.title

    # owner is serialized as user's profile url
    assert '/api/profiles/{}/'.format(cal_instance.owner.id) in cal_dict['owner']

    # members are each serialized as profile url
    for member in cal_instance.members.all():
        url_regex = re.compile('^http://.+/api/profiles/{}/$'.format(member.id))
        assert filter(url_regex, cal_dict['members'])


def test_get_calendars_list(client, create_calendars):
    cal1 = Calendar.objects.get(owner__username='user1')
    cal2 = Calendar.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.get('/api/calendars/{}/'.format(cal1.id))
    assert response.status_code == 401

    # login as user1, gets 200, can get own calendar
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/calendars/', HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    calendars_json = json.loads(response.content.decode())
    # user1 is the only member to cal1
    assert len(calendars_json) == 1
    check_calendar_is_instance(calendars_json[0], cal1)

    # login as user2, gets 200, can get own calendar
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.get(
        '/api/calendars/', HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    calendars_json = json.loads(response.content.decode())
    # user2 is the only member to cal2
    assert len(calendars_json) == 1
    check_calendar_is_instance(calendars_json[0], cal2)


def test_get_calendar_by_id(client, create_calendars):
    cal1 = Calendar.objects.get(owner__username='user1')
    cal2 = Calendar.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.get('/api/calendars/{}/'.format(cal1.id))
    assert response.status_code == 401

    # login as user1, gets 200, can get own calendar
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/calendars/{}/'.format(cal1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    cal_json1 = json.loads(response.content.decode())
    check_calendar_is_instance(cal_json1, cal1)
    # cannot get user2's calendar
    response = client.get(
        '/api/calendars/{}/'.format(cal2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404

    # login as user2, gets 200, can get own calendar
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.get(
        '/api/calendars/{}/'.format(cal2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    cal_json2 = json.loads(response.content.decode())
    check_calendar_is_instance(cal_json2, cal2)
    # cannot get user1's calendar
    response = client.get(
        '/api/calendars/{}/'.format(cal1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 404


def test_post_calendars(client, create_profiles):
    cal3_info = {'title': 'calendar 3 for view', 'owner_color_hex': '000000'}

    # anon user gets 401
    response = client.post('/api/calendars/', cal3_info)
    assert response.status_code == 401

    # login as user1, gets 200, can post
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    cal3_info = {'title': 'calendar 3 for view', 'owner_color_hex': '000000'}
    response = client.post(
        '/api/calendars/', cal3_info,
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 201
    assert Calendar.objects.count() == 1

    # a membership of owner and calendar is auto saved
    mbship1 = Membership.objects.get(color_hex='000000')
    assert mbship1.calendar.title == 'calendar 3 for view'
    assert mbship1.member.username == 'user1'

    # login as user2
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    cal4_info = {'title': 'calendar 4 for view', 'owner_color_hex': 'FFFFFF'}
    response2 = client.post(
        '/api/calendars/', cal4_info,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 201
    assert Calendar.objects.count() == 2
    # a membership of owner and calendar is auto saved
    mbship2 = Membership.objects.get(color_hex='FFFFFF')
    assert mbship2.calendar.title == 'calendar 4 for view'
    assert mbship2.member.username == 'user2'


def test_delete_calendars(client, create_calendars):
    cal1 = Calendar.objects.get(owner__username='user1')
    cal2 = Calendar.objects.get(owner__username='user2')

    # anon user gets 401
    response = client.delete('/api/calendars/{}/'.format(cal1.id))
    assert response.status_code == 401
    assert Calendar.objects.count() == 2

    # login as user1 gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.delete(
        '/api/calendars/{}/'.format(cal1.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 204
    assert Calendar.objects.count() == 1
    # cannot delete user2's calendar
    response = client.delete(
        '/api/calendars/{}/'.format(cal2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404

    # login as user2 gets 200
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.delete(
        '/api/calendars/{}/'.format(cal2.id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 204
    assert Calendar.objects.count() == 0


def test_patch_calendars(client, create_calendars):
    cal1 = Calendar.objects.get(owner__username='user1')

    # anon user gets 401
    response = client.patch(
        '/api/calendars/{}/'.format(cal1.id),
        data=json.dumps({'title': 'changed title'}),
        content_type='application/json')
    assert response.status_code == 401

    # login as user1 gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.patch(
        '/api/calendars/{}/'.format(cal1.id),
        data=json.dumps({'title': 'changed title'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    cal1 = Calendar.objects.get(owner__username='user1')
    assert cal1.title == 'changed title'
    # cannot patch user2's calendar
    cal2 = Calendar.objects.get(owner__username='user2')
    response = client.patch(
        '/api/calendars/{}/'.format(cal2.id),
        data=json.dumps({'title': 'changed title'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 404
    cal1 = Calendar.objects.get(owner__username='user2')
    assert cal1.title == 'calendar 2'
