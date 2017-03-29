
from calendars.models import Calendar
from memberships.models import Membership


def test_can_save_and_retrieve_memberships(create_calendars):
    saved_memberships = Membership.objects.all()
    assert len(saved_memberships) == 2

    # First membership is created with calendar1 and normal_user1
    mbship1 = Membership.objects.get(member__username='user1')
    cal1 = Calendar.objects.get(owner__username='user1')
    assert mbship1.calendar == cal1
    assert mbship1.member in cal1.members.all()

    # second membership is created with calendar2 and normal_user2
    mbship2 = Membership.objects.get(member__username='user2')
    cal2 = Calendar.objects.get(owner__username='user2')
    assert mbship2.calendar == cal2
    assert mbship2.member in cal2.members.all()
