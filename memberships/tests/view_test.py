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


def test_get_memberships_list(admin_client, client, create_memberships):
    # anon user gets 403
    response = client.get('/api/memberships/')
    assert response.status_code == 403

    # login as normal_user1 and gets 200
    client.login(username='user1', password='qwerty123')
    response = client.get('/api/memberships/')
    assert response.status_code == 200
    # only sees its own memberships
    mbships_json = json.loads(response.content.decode())
    assert len(mbships_json) == 1
    retrieved_mbship = mbships_json[0]
    saved_mbship = Membership.objects.get(color_hex=retrieved_mbship['color_hex'])
    check_mbship_dict_is_instance(retrieved_mbship, saved_mbship)

    # login as normal_user2 and gets 200
    client.logout()
    client.login(username='user2', password='qwerty123')
    response = client.get('/api/memberships/')
    assert response.status_code == 200
    # only sees its own memberships
    mbships_json = json.loads(response.content.decode())
    assert len(mbships_json) == 1
    retrieved_mbship = mbships_json[0]
    saved_mbship = Membership.objects.get(color_hex=retrieved_mbship['color_hex'])
    check_mbship_dict_is_instance(retrieved_mbship, saved_mbship)

    # admin sees all memberships
    response = admin_client.get('/api/memberships/')
    assert response.status_code == 200
    mbships_json = json.loads(response.content.decode())
    assert len(mbships_json) == 2


def test_get_membership_by_id(
        admin_client, client, normal_user1, normal_user2, create_memberships):
    saved_mbship1 = Membership.objects.get(member_id=normal_user1.id)
    saved_mbship2 = Membership.objects.get(member_id=normal_user2.id)

    # anon user gets 403
    response = client.get('/api/memberships/{}/'.format(saved_mbship1.id))
    assert response.status_code == 403

    # login as normal_user1 and gets 200
    client.login(username='user1', password='qwerty123')
    response = client.get('/api/memberships/{}/'.format(saved_mbship1.id))
    assert response.status_code == 200
    retrieved_mbship = json.loads(response.content.decode())
    check_mbship_dict_is_instance(retrieved_mbship, saved_mbship1)
    # normal_user1 cannot get normal_user2's membership
    response = client.get('/api/memberships/{}/'.format(saved_mbship2.id))
    assert response.status_code == 404

    # login as normal_user2 and gets 200
    client.logout()
    client.login(username='user2', password='qwerty123')
    response = client.get('/api/memberships/{}/'.format(saved_mbship2.id))
    assert response.status_code == 200
    retrieved_mbship = json.loads(response.content.decode())
    check_mbship_dict_is_instance(retrieved_mbship, saved_mbship2)
    # normal_user2 cannot get normal_user1's membership
    response = client.get('/api/memberships/{}/'.format(saved_mbship1.id))
    assert response.status_code == 404

    # admin sees both
    response = admin_client.get('/api/memberships/{}/'.format(saved_mbship1.id))
    assert response.status_code == 200
    response = admin_client.get('/api/memberships/{}/'.format(saved_mbship2.id))
    assert response.status_code == 200


def test_post_memberships(client, create_calendars, create_profiles):
    cal1, cal2 = Calendar.objects.all()
    complete_profile, incomplete_profile = Profile.objects.all()

    mbship1_data = {
        'color_hex': '000000',
        'calendar': '/api/calendars/{}/'.format(cal1.id),
        'member': '/api/profiles/{}/'.format(incomplete_profile.user_id)}
    mbship2_data = {
        'color_hex': 'FFFFFF',
        'calendar': '/api/calendars/{}/'.format(cal2.id),
        'member': '/api/profiles/{}/'.format(complete_profile.user_id)}

    # anon user gets 403
    response = client.post('/api/memberships/', mbship1_data)
    assert response.status_code == 403

    # login as normal_user1, gets 200
    client.login(username='user1', password='qwerty123')
    response = client.post('/api/memberships/', mbship1_data)
    assert response.status_code == 201
    assert Membership.objects.count() == 1
    # but cannot post membership with calendar owned by normal_user2
    response = client.post('/api/memberships/', mbship2_data)
    assert response.status_code == 400    # cal2 not in queryset

    # login as normal_user2 and gets 200
    client.logout()
    client.login(username='user2', password='qwerty123')
    response = client.post('/api/memberships/', mbship2_data)
    assert response.status_code == 201
    assert Membership.objects.count() == 2
    # but cannot post membership with calendar owned by normal_user2
    response = client.post('/api/memberships/', mbship1_data)
    assert response.status_code == 400    # cal1 not in queryset


def test_delete_memberships(client, normal_user1, normal_user2, create_memberships):
    mbship1 = Membership.objects.get(member_id=normal_user1.id)
    mbship2 = Membership.objects.get(member_id=normal_user2.id)

    # anon user gets 403
    response = client.delete('/api/memberships/{}/'.format(mbship1.id))
    assert response.status_code == 403

    # login as normal_user1, gets 200
    client.login(username='user1', password='qwerty123')
    response = client.delete('/api/memberships/{}/'.format(mbship1.id))
    assert response.status_code == 204
    assert Membership.objects.count() == 1
    # still can't delete normal_user2's membership
    response = client.delete('/api/memberships/{}/'.format(mbship2.id))
    assert response.status_code == 404

    # login as normal_user2 and gets 200
    client.logout()
    client.login(username='user2', password='qwerty123')
    response = client.delete('/api/memberships/{}/'.format(mbship2.id))
    assert response.status_code == 204
    assert Membership.objects.count() == 0


def test_patch_membership(client, normal_user1, normal_user2, create_memberships):
    mbship1 = Membership.objects.get(member_id=normal_user1.id)
    mbship2 = Membership.objects.get(member_id=normal_user2.id)

    # anon user gets 403
    response = client.patch(
        '/api/memberships/{}/'.format(mbship1.id),
        data=json.dumps({'color_hex': '111111'}),
        content_type='application/json')
    assert response.status_code == 403

    # login as normal_user1, gets 200
    client.login(username='user1', password='qwerty123')
    response = client.patch(
        '/api/memberships/{}/'.format(mbship1.id),
        data=json.dumps({'color_hex': '111111'}),
        content_type='application/json')
    assert response.status_code == 200
    mbship1 = Membership.objects.get(member_id=normal_user1.id)
    assert mbship1.color_hex == '111111'
    # still cannot patch to normal_user2's membership
    response = client.patch(
        '/api/memberships/{}/'.format(mbship2.id),
        data=json.dumps({'color_hex': 'EEEEEE'}),
        content_type='application/json')
    assert response.status_code == 404


def test_cannot_use_repeated_color_in_one_calendar(client, create_memberships):
    # try to create another Membership instance with same color_hex and calendar
    cal1_id = Calendar.objects.first().id
    complete_profile_id = Profile.objects.first().user_id
    mbship1_data = {
        'color_hex': '000000',
        'calendar': '/api/calendars/{}/'.format(cal1_id),
        'member': '/api/profiles/{}/'.format(complete_profile_id)}

    # login as normal_user1
    client.login(username='user1', password='qwerty123')
    response = client.post('/api/memberships/', mbship1_data)
    assert response.status_code == 400
    err_msg = json.loads(response.content.decode())
    assert 'Members cannot have the same color.' in err_msg['non_field_errors']
