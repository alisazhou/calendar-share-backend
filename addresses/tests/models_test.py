import pytest

from addresses.models import Address



@pytest.mark.django_db
def test_can_save_and_retrieve_addresses(address1, address2, create_addresses):
    saved_addresses = Address.objects.all()
    assert len(saved_addresses) == 2

    saved_address1 = saved_addresses[0]
    assert saved_address1.street == address1['street']
    assert saved_address1.city == address1['city']
    assert saved_address1.state == address1['state']
    assert saved_address1.zipcode == address1['zipcode']

    saved_address2 = saved_addresses[1]
    assert saved_address2.street == address2['street']
    assert saved_address2.city == address2['city']
    assert saved_address2.state == address2['state']
    assert saved_address2.zipcode == address2['zipcode']
