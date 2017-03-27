import pytest

from addresses.models import Address
from addresses.tests.address_plugins import check_address_is_instance


@pytest.mark.django_db
def test_can_save_and_retrieve_addresses(address1, address2, create_addresses):
    saved_addresses = Address.objects.all()
    assert len(saved_addresses) == 2

    saved_address1 = saved_addresses[0]
    check_address_is_instance(address1, saved_address1)

    saved_address2 = saved_addresses[1]
    check_address_is_instance(address2, saved_address2)
