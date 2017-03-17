import json
import pytest

from profiles.models import Profile


ADDRESS_ATTRS = ('street', 'city', 'state', 'zipcode')
USER_ATTRS = ('username', 'email', 'first_name', 'last_name')

def check_profile_is_instance(profile_dict, profile_instance):
    # check if user matches (required)
    for k in USER_ATTRS:
        assert profile_dict[k] == getattr(profile_instance.user, k)
    # check if address matches
    if profile_instance.address:
        for k in ADDRESS_ATTRS:
            assert profile_dict[k] == getattr(profile_instance.address, k)
    else:
        for k in ADDRESS_ATTRS:
            assert profile_dict[k] == None
    # check if other fields match
    if profile_instance.bday:
        bday_str = '{:%Y-%m-%d}'.format(profile_instance.bday)
        assert profile_dict['bday'] == bday_str
    else:
        assert profile_dict['bday'] == None
    assert profile_dict['phone'] == getattr(profile_instance, 'phone', None)


def test_get_profiles_list(client, create_profiles):
    response = client.get('/api/profiles/')
    assert response.status_code == 200

    profiles_json = json.loads(response.content.decode())
    assert len(profiles_json) == Profile.objects.count()

    profile1, profile2 = Profile.objects.all()
    check_profile_is_instance(profiles_json[0], profile1)
    check_profile_is_instance(profiles_json[1], profile2)


def test_get_profile_by_id(client, create_profiles):
    profile1, profile2 = Profile.objects.all()

    response1 = client.get('/api/profiles/1/')
    assert response1.status_code == 200
    profile_json1 = json.loads(response1.content.decode())
    check_profile_is_instance(profile_json1, profile1)

    response2 = client.get('/api/profiles/2/')
    assert response2.status_code == 200
    profile_json2 = json.loads(response2.content.decode())
    check_profile_is_instance(profile_json2, profile2)


@pytest.mark.django_db
def test_post_profiles(
        client, complete_profile_for_view, incomplete_profile_for_view):
    response1 = client.post('/api/profiles/', complete_profile_for_view)
    assert response1.status_code == 201
    assert Profile.objects.count() == 1

    response2 = client.post('/api/profiles/', incomplete_profile_for_view)
    assert response2.status_code == 201
    assert Profile.objects.count() == 2


def test_delete_profiles(client, create_profiles):
    response1 = client.delete('/api/profiles/1/')
    assert response1.status_code == 204
    assert Profile.objects.count() == 1

    response2 = client.delete('/api/profiles/2/')
    assert response2.status_code == 204
    assert Profile.objects.count() == 0


def test_patch_profile(client, create_profiles):
    # Changing profile1 existing field
    response1 = client.patch(
        '/api/profiles/1/',
        data=json.dumps({'phone': '9177654321'}),
        content_type='application/json')
    profile1 = Profile.objects.first()
    assert profile1.phone == '9177654321'
    # check that other fields remain the same
    assert '{:%Y-%m-%d}'.format(profile1.bday) == '2017-03-17'

    # Changing profile2 currently empty field
    response2 = client.patch(
        '/api/profiles/2/',
        data=json.dumps({'phone': '9491234567'}),
        content_type='application/json')
    profile2 = Profile.objects.all()[1]
    assert profile2.phone == '9491234567'
    # check that other fields remain empty
    assert profile2.bday == None
