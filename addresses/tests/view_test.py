import json
import pytest

from addresses.models import Address
from addresses.tests.address_plugins import check_address_is_instance
from common.test_helpers import get_user_token


def test_get_addresses_list(admin_user, client, create_addresses):
    saved_address1, saved_address2 = Address.objects.all()

    # anon user gets 401 forbidden
    response = client.get('/api/addresses/')
    assert response.status_code == 401

    # login as normal_user1, gets 200
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/addresses/', HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    # normal_user1 only sees their own address
    addresses_json = json.loads(response.content.decode())
    assert len(addresses_json) == 1
    check_address_is_instance(addresses_json[0], saved_address1)

    # login as normal_user2, gets 200
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.get(
        '/api/addresses/', HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    # normal_user2 only sees their own address
    addresses_json = json.loads(response.content.decode())
    assert len(addresses_json) == 1
    check_address_is_instance(addresses_json[0], saved_address2)

    # admin sees all addresses
    admin_token = get_user_token(client, 'admin', 'password')
    response = client.get(
        '/api/addresses/', HTTP_AUTHORIZATION='Token {}'.format(admin_token))
    assert response.status_code == 200
    addresses_json = json.loads(response.content.decode())
    assert len(addresses_json) == 2
    check_address_is_instance(addresses_json[0], saved_address1)
    check_address_is_instance(addresses_json[1], saved_address2)


def test_get_address_by_id(admin_user, client, create_addresses):
    address1, address2 = Address.objects.all()

    # anon user gets 401 forbidden
    response = client.get('/api/addresses/{}/'.format(address1.user_id))
    assert response.status_code == 401

    # login as normal_user1, gets 200 and sees own address
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.get(
        '/api/addresses/{}/'.format(address1.user_id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    address1_json = json.loads(response.content.decode())
    check_address_is_instance(address1_json, address1)

    # login as normal_user2, gets 200 and sees own address
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response = client.get(
        '/api/addresses/{}/'.format(address2.user_id),
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response.status_code == 200
    address2_json = json.loads(response.content.decode())
    check_address_is_instance(address2_json, address2)

    # admin can see address1
    admin_token = get_user_token(client, 'admin', 'password')
    response = client.get(
        '/api/addresses/{}/'.format(address1.user_id),
        HTTP_AUTHORIZATION='Token {}'.format(admin_token))
    assert response.status_code == 200
    address1_json = json.loads(response.content.decode())
    check_address_is_instance(address1_json, address1)
    # admin can also see address2
    response = client.get(
        '/api/addresses/{}/'.format(address2.user_id),
        HTTP_AUTHORIZATION='Token {}'.format(admin_token))
    assert response.status_code == 200
    address2_json = json.loads(response.content.decode())
    check_address_is_instance(address2_json, address2)


@pytest.mark.django_db
def test_post_addresses(client, address1, address2):
    # post address with user1's token
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response1 = client.post(
        '/api/addresses/', address1,
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response1.status_code == 201
    assert Address.objects.count() == 1

    # post address with user2's token
    user2_token = get_user_token(client, 'user2', 'qwerty123')
    response2 = client.post(
        '/api/addresses/', address2,
        HTTP_AUTHORIZATION='Token {}'.format(user2_token))
    assert response2.status_code == 201
    assert Address.objects.count() == 2

    address_instances = Address.objects.all()
    check_address_is_instance(address1, address_instances[0])
    check_address_is_instance(address2, address_instances[1])


def test_delete_addresses(admin_user, client, create_addresses):
    address1, address2 = Address.objects.all()

    # anon user gets 401
    response = client.delete('/api/addresses/{}/'.format(address1.user_id))
    assert response.status_code == 401
    assert Address.objects.count() == 2

    # login as normal_user1, can delete own address
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.delete(
        '/api/addresses/{}/'.format(address1.user_id),
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 204
    assert Address.objects.count() == 1

    # login as admin, can delete user address
    admin_token = get_user_token(client, 'admin', 'password')
    response = client.delete(
        '/api/addresses/{}/'.format(address2.user_id),
        HTTP_AUTHORIZATION='Token {}'.format(admin_token))
    assert response.status_code == 204
    assert Address.objects.count() == 0


def test_patch_address(client, create_addresses):
    address1 = Address.objects.first()

    # anon user gets 401
    response = client.patch(
        '/api/addresses/{}/'.format(address1.user_id),
        data=json.dumps({'city': 'New York'}),
        content_type='application/json')
    assert response.status_code == 401

    # login as normal_user1, can patch own address
    user1_token = get_user_token(client, 'user1', 'qwerty123')
    response = client.patch(
        '/api/addresses/{}/'.format(address1.user_id),
        data=json.dumps({'city': 'New York'}),
        content_type='application/json',
        HTTP_AUTHORIZATION='Token {}'.format(user1_token))
    assert response.status_code == 200
    address1 = Address.objects.first()
    assert address1.city == 'New York'
