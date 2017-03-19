import json
import re

from calendars.models import Calendar
from profiles.models import Profile


def check_calendar_is_instance(cal_dict, cal_instance):
    assert cal_dict['title'] == cal_instance.title

    # owner is serialized as user's profile url
    owner_profile = Profile.objects.get(user_id=cal_instance.owner.id)
    assert '/api/profiles/{}/'.format(owner_profile.id) in cal_dict['owner']

    # members are each serialized as profile url
    for member in cal_instance.members.all():
        url_regex = re.compile('^http://.+/api/profiles/{}/$'.format(member.id))
        assert filter(url_regex, cal_dict['members'])


def test_get_calendars_list(client, create_calendars, create_memberships):
    response = client.get('/api/calendars/')
    assert response.status_code == 200

    calendars_json = json.loads(response.content.decode())
    assert len(calendars_json) == 2

    cal1, cal2 = Calendar.objects.all()
    check_calendar_is_instance(calendars_json[0], cal1)
    check_calendar_is_instance(calendars_json[1], cal2)


def test_get_calendar_by_id(client, create_calendars):
    cal1, cal2 = Calendar.objects.all()

    response1 = client.get('/api/calendars/{}/'.format(cal1.id))
    assert response1.status_code == 200
    cal_json1 = json.loads(response1.content.decode())
    check_calendar_is_instance(cal_json1, cal1)

    response2 = client.get('/api/calendars/{}/'.format(cal2.id))
    assert response2.status_code == 200
    cal_json2 = json.loads(response2.content.decode())
    check_calendar_is_instance(cal_json2, cal2)


def test_post_calendars(admin_client):
    cal3_info = {'title': 'calendar 3 for view'}
    # view captures the logged-in user creating this calendar as its owner
    response1 = admin_client.post('/api/calendars/', cal3_info)
    assert response1.status_code == 201
    assert Calendar.objects.count() == 1

    cal4_info = {'title': 'calendar 4 for view'}
    response2 = admin_client.post('/api/calendars/', cal4_info)
    assert response2.status_code == 201
    assert Calendar.objects.count() == 2


def test_delete_calendars(client, create_calendars):
    cal1, cal2 = Calendar.objects.all()

    client.delete('/api/calendars/{}/'.format(cal1.id))
    assert Calendar.objects.count() == 1

    client.delete('/api/calendars/{}/'.format(cal2.id))
    assert Calendar.objects.count() == 0


def test_patch_address(client, create_calendars):
    cal1 = Calendar.objects.first()
    orig_owner = cal1.owner

    response = client.patch(
        '/api/calendars/{}/'.format(cal1.id),
        data=json.dumps({'title': 'changed title'}),
        content_type='application/json')
    assert response.status_code == 200
    cal1 = Calendar.objects.first()
    assert cal1.title == 'changed title'
    assert cal1.owner == orig_owner
