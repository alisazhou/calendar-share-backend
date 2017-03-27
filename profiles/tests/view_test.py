import json
import pytest

from profiles.models import Profile


USER_ATTRS = ('username', 'email', 'first_name', 'last_name')


def check_profile_is_instance(profile_dict, profile_instance):
    # check if user matches (required)
    for k in USER_ATTRS:
        assert profile_dict[k] == getattr(profile_instance.user, k)

    # check if other fields match
    if profile_instance.bday:
        bday_str = '{:%Y-%m-%d}'.format(profile_instance.bday)
        assert profile_dict['bday'] == bday_str
    else:
        assert profile_dict['bday'] is None
    assert profile_dict['phone'] == getattr(profile_instance, 'phone', None)


def test_get_profiles_list(admin_client, client, create_profiles):
    profile1, profile2 = Profile.objects.all()

    # anon user gets 403 forbidden
    response = client.get('/api/profiles/')
    assert response.status_code == 403

    # login as normal_user1, can see own profile
    client.login(username='user1', password='qwerty123')
    response = client.get('/api/profiles/')
    assert response.status_code == 200
    profiles_json = json.loads(response.content.decode())
    assert len(profiles_json) == 1
    check_profile_is_instance(profiles_json[0], profile1)

    # login as normal_user2, can see own profile
    client.logout()
    client.login(username='user2', password='qwerty123')
    response = client.get('/api/profiles/')
    assert response.status_code == 200
    profiles_json = json.loads(response.content.decode())
    assert len(profiles_json) == 1
    check_profile_is_instance(profiles_json[0], profile2)

    # login as admin, can see all profiles
    response = admin_client.get('/api/profiles/')
    assert response.status_code == 200
    profiles_json = json.loads(response.content.decode())
    assert len(profiles_json) == 2
    check_profile_is_instance(profiles_json[0], profile1)
    check_profile_is_instance(profiles_json[1], profile2)


def test_get_profile_by_id(admin_client, client, create_profiles):
    profile1, profile2 = Profile.objects.all()

    # anon user gets 403 forbidden
    response = client.get('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 403

    # login as normal_user1, can see own profile
    client.login(username='user1', password='qwerty123')
    response = client.get('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 200
    profile_json1 = json.loads(response.content.decode())
    check_profile_is_instance(profile_json1, profile1)
    # still can't see others' profiles
    response = client.get('/api/profiles/{}/'.format(profile2.user_id))
    assert response.status_code == 404    # 404 because not part of queryset

    # login as normal_user2, can see own profile
    client.login(username='user2', password='qwerty123')
    response = client.get('/api/profiles/{}/'.format(profile2.user_id))
    assert response.status_code == 200
    profile_json2 = json.loads(response.content.decode())
    check_profile_is_instance(profile_json2, profile2)
    # still can't see others' profiles
    response = client.get('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 404    # 404 because not part of queryset

    # admin can see normal_user1's profile
    response = admin_client.get('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 200
    profile_json1 = json.loads(response.content.decode())
    check_profile_is_instance(profile_json1, profile1)
    # admin can also see normal_user2's profile
    response = admin_client.get('/api/profiles/{}/'.format(profile2.user_id))
    assert response.status_code == 200
    profile_json2 = json.loads(response.content.decode())
    check_profile_is_instance(profile_json2, profile2)


@pytest.mark.django_db
def test_post_profiles(
        client, complete_profile_for_view, incomplete_profile_for_view):
    # anon users can create profiles
    response = client.post('/api/profiles/', complete_profile_for_view)
    assert response.status_code == 201
    assert Profile.objects.count() == 1

    response2 = client.post('/api/profiles/', incomplete_profile_for_view)
    assert response2.status_code == 201
    assert Profile.objects.count() == 2


def test_delete_profiles(client, create_profiles):
    profile1, profile2 = Profile.objects.all()

    # anon user gets 403 forbidden
    response = client.delete('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 403

    # login as normal_user1, can see own profile
    client.login(username='user1', password='qwerty123')
    response = client.delete('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 204
    assert Profile.objects.count() == 1
    # still cannot delete normal_user2's profile
    response = client.delete('/api/profiles/{}/'.format(profile1.user_id))
    assert response.status_code == 404    # 404 because not in queryset
    assert Profile.objects.count() == 1

    # login as normal_user2, can see own profile
    client.logout()
    client.login(username='user2', password='qwerty123')
    response = client.delete('/api/profiles/{}/'.format(profile2.user_id))
    assert response.status_code == 204
    assert Profile.objects.count() == 0


def test_patch_profile(admin_client, client, create_profiles):
    profile1, profile2 = Profile.objects.all()

    # anon user gets 403
    response = client.patch(
        '/api/profiles/{}/'.format(profile1.user_id),
        data=json.dumps({'phone': '9177654321'}),
        content_type='application/json')
    assert response.status_code == 403

    # login as normal_user1, can see own profile
    client.login(username='user1', password='qwerty123')
    response = client.patch(
        '/api/profiles/{}/'.format(profile1.user_id),
        data=json.dumps({'phone': '9177654321'}),
        content_type='application/json')
    assert response.status_code == 200

    # patch has worked
    profile1 = Profile.objects.first()
    assert profile1.phone == '9177654321'
    # check that other fields remain the same
    assert '{:%Y-%m-%d}'.format(profile1.bday) == '2017-03-17'

    # admin can patch
    response = admin_client.patch(
        '/api/profiles/{}/'.format(profile2.user_id),
        data=json.dumps({'phone': '9491234567'}),
        content_type='application/json')
    assert response.status_code == 200

    profile2 = Profile.objects.all()[1]
    assert profile2.phone == '9491234567'
    # check that other fields remain empty
    assert profile2.bday is None
