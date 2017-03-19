
from calendars.models import Calendar
from memberships.models import Membership
from profiles.models import Profile


def test_can_save_and_retrieve_memberships(create_memberships):
    saved_memberships = Membership.objects.all()
    cal1, cal2 = Calendar.objects.all()
    complete_profile, incomplete_profile = Profile.objects.all()
    assert len(saved_memberships) == 2

    # First membership is created with calendar1 and incomplete_profile
    membership1 = saved_memberships[0]
    assert membership1.calendar_id == cal1.id
    assert membership1.member_id == incomplete_profile.id
    # check now calendar1 has incomplete_profile as a member
    assert incomplete_profile in cal1.members.all()

    # second membership is created with calendar2 and complete_profile
    membership2 = saved_memberships[1]
    assert membership2.calendar_id == cal2.id
    assert membership2.member_id == complete_profile.id
    # check now calendar2 has complete_profile as a member
    assert complete_profile in cal2.members.all()
