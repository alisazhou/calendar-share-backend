import json
import pytest

from addresses.models import Address



def check_address_is_instance(address_dict, address_instance):
    # address_instance has an autogenerated 'id' key
    for k, v in address_dict.items():
        assert getattr(address_instance, k) == v


def test_get_addresses_list(client, create_addresses):
    response = client.get('/api/addresses/')
    assert response.status_code == 200

    addresses_json = json.loads(response.content.decode())
    address_instances = Address.objects.all()
    assert len(addresses_json) == 2
    check_address_is_instance(addresses_json[0], address_instances[0])
    check_address_is_instance(addresses_json[1], address_instances[1])


def test_get_address_by_id(client, create_addresses):
    address_instances = Address.objects.all()

    response1 = client.get('/api/addresses/1/')
    assert response1.status_code == 200
    address1_json = json.loads(response1.content.decode())
    check_address_is_instance(address1_json, address_instances[0])

    response2 = client.get('/api/addresses/2/')
    assert response2.status_code == 200
    address2_json = json.loads(response2.content.decode())
    check_address_is_instance(address2_json, address_instances[1])


@pytest.mark.django_db
def test_post_addresses(client, address1, address2):
    response1 = client.post('/api/addresses/', address1)
    assert response1.status_code == 201
    assert Address.objects.count() == 1

    response2 = client.post('/api/addresses/', address2)
    assert response2.status_code == 201
    assert Address.objects.count() == 2

    address_instances = Address.objects.all()
    check_address_is_instance(address1, address_instances[0])
    check_address_is_instance(address2, address_instances[1])


def test_delete_addresses(client, create_addresses):
    response1 = client.delete('/api/addresses/1/')
    assert response1.status_code == 204
    assert Address.objects.count() == 1

    response2 = client.delete('/api/addresses/2/')
    assert response2.status_code == 204
    assert Address.objects.count() == 0


def test_patch_address(client, create_addresses):
    response = client.patch(
        '/api/addresses/1/',
        data=json.dumps({'city':'New York'}),
        content_type='application/json')
    assert response.status_code == 200
    address1 = Address.objects.first()
    assert address1.city == 'New York'
