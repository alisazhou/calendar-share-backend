import json

from calendars.models import Calendar
from memberships.models import Membership
from profiles.models import Profile


def check_mbship_dict_is_instance(mbship_dict, mbship_instance):
    # check if color_hex match
    assert mbship_dict['color_hex'] == mbship_instance.color_hex

    # check if calendar match, in dict calendar is serialized as its url
    cal_id = mbship_instance.calendar_id
    assert '/api/calendars/{}/'.format(cal_id) in mbship_dict['calendar']

    # check if member match, in dict member is serialized as profile url
    member_id = mbship_instance.member_id
    assert '/api/profiles/{}/'.format(member_id) in mbship_dict['member']


def test_get_memberships_list(client, create_memberships):
    response = client.get('/api/memberships/')
    assert response.status_code == 200

    mbships_json = json.loads(response.content.decode())
    assert len(mbships_json) == 2

    mbship1, mbship2 = Membership.objects.all()
    check_mbship_dict_is_instance(mbships_json[0], mbship1)
    check_mbship_dict_is_instance(mbships_json[1], mbship2)


def test_get_membership_by_id(client, create_memberships):
    mbship1, mbship2 = Membership.objects.all()

    response1 = client.get('/api/memberships/{}/'.format(mbship1.id))
    assert response1.status_code == 200
    mbship_json1 = json.loads(response1.content.decode())
    check_mbship_dict_is_instance(mbship_json1, mbship1)

    response2 = client.get('/api/memberships/{}/'.format(mbship2.id))
    assert response2.status_code == 200
    mbship_json2 = json.loads(response2.content.decode())
    check_mbship_dict_is_instance(mbship_json2, mbship2)


def test_post_memberships(client, create_calendars, create_profiles):
    cal1, cal2 = Calendar.objects.all()
    complete_profile, incomplete_profile = Profile.objects.all()

    mbship1_data = {
        'color_hex': '000000',
        'calendar': '/api/calendars/{}/'.format(cal1.id),
        'member': '/api/profiles/{}/'.format(incomplete_profile.id)}
    response1 = client.post('/api/memberships/', mbship1_data)
    assert response1.status_code == 201
    assert Membership.objects.count() == 1

    mbship2_data = {
        'color_hex': 'FFFFFF',
        'calendar': '/api/calendars/{}/'.format(cal2.id),
        'member': '/api/profiles/{}/'.format(complete_profile.id)}
    response2 = client.post('/api/memberships/', mbship2_data)
    assert response2.status_code == 201
    assert Membership.objects.count() == 2


def test_delete_memberships(client, create_memberships):
    mbship1, mbship2 = Membership.objects.all()

    response1 = client.delete('/api/memberships/{}/'.format(mbship1.id))
    assert response1.status_code == 204
    assert Membership.objects.count() == 1

    response2 = client.delete('/api/memberships/{}/'.format(mbship2.id))
    assert response2.status_code == 204
    assert Membership.objects.count() == 0


def test_patch_membership(client, create_memberships):
    mbship1, mbship2 = Membership.objects.all()

    client.patch(
        '/api/memberships/{}/'.format(mbship1.id),
        data=json.dumps({'color_hex': '111111'}),
        content_type='application/json')
    mbship1 = Membership.objects.first()
    assert mbship1.color_hex == '111111'

    client.patch(
        '/api/memberships/{}/'.format(mbship2.id),
        data=json.dumps({'color_hex': 'EEEEEE'}),
        content_type='application/json')
    mbship2 = Membership.objects.all()[1]
    assert mbship2.color_hex == 'EEEEEE'


def test_cannot_use_repeated_color_in_one_calendar(client, create_memberships):
    # try to create another Membership instance with same color_hex and calendar
    cal1_id = Calendar.objects.first().id
    complete_profile_id = Profile.objects.first().id
    mbship1_data = {
        'color_hex': '000000',
        'calendar': '/api/calendars/{}/'.format(cal1_id),
        'member': '/api/profiles/{}/'.format(complete_profile_id)}
    response = client.post('/api/memberships/', mbship1_data)
    assert response.status_code == 400
    err_msg = json.loads(response.content.decode())
    assert 'Members cannot have the same color.' in err_msg['non_field_errors']
