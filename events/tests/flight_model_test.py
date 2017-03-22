from events.models import Flight
from events.tests.event_plugins import check_event_is_instance


def test_can_save_and_retrieve_flights(flight1, flight2, create_flights):
    assert Flight.objects.count() == 2

    saved_flight1 = Flight.objects.get(title='flight 1')
    check_event_is_instance(flight1, saved_flight1)

    saved_flight2 = Flight.objects.get(title='flight 2')
    check_event_is_instance(flight2, saved_flight2)
