from django.db.utils import IntegrityError
import pytest

from profiles.models import Profile
from addresses.models import Address


@pytest.mark.django_db
def test_can_save_and_retrieve_profiles(
        complete_profile, incomplete_profile, create_profiles):
    saved_profiles = Profile.objects.all()
    assert len(saved_profiles) == 2

    # complete_profile, created with address1, normal_user1
    saved_profile1 = saved_profiles[0]
    address1 = Address.objects.first()
    assert saved_profile1.address_id == address1.id
    bday_str = '{:%Y-%m-%d}'.format(saved_profile1.bday)
    assert bday_str == complete_profile['bday']
    assert saved_profile1.phone == complete_profile['phone']
    assert saved_profile1.user.username == 'user1'

    # incomplete_profile, created with normal_user2
    saved_profile2 = saved_profiles[1]
    assert saved_profile2.user.username == 'user2'


def test_cannot_save_with_same_phone(
        complete_profile, create_profiles, django_user_model):
    normal_user3 = django_user_model.objects.create(
        username='user3', password='qwerty123')
    with pytest.raises(IntegrityError):
        Profile.objects.create(
            phone=complete_profile['phone'], user=normal_user3)


def test_cannot_save_with_same_user(create_profiles, normal_user1):
    # complete_profile is created with normal_user1
    with pytest.raises(IntegrityError):
        Profile.objects.create(user=normal_user1)
