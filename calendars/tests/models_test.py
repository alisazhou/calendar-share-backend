from calendars.models import Calendar
from memberships.models import Membership


def test_can_save_and_retrieve_calendars(calendar1, calendar2, create_calendars):
    saved_cals = Calendar.objects.all()
    assert len(saved_cals) == 2

    saved_cal1 = saved_cals[0]
    assert saved_cal1.title == calendar1['title']
    # calendar1 is created with normal_user1
    assert saved_cal1.owner.username == 'user1'

    saved_cal2 = saved_cals[1]
    assert saved_cal2.title == calendar2['title']
    # calendar2 is created with normal_user2
    assert saved_cal2.owner.username == 'user2'


def test_can_add_members_by_creating_membership_instances(normal_user2, create_calendars, create_profiles):
    cal1 = Calendar.objects.first()
    assert cal1.members.count() == 0

    Membership.objects.create(
        color_hex='000000', member=normal_user2, calendar=cal1)
    assert cal1.members.count() == 1
    assert cal1.members.first() == normal_user2
