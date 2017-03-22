from events.models import Flight
from events.tests.event_plugins import check_date_time_object_and_str_are_the_same


def check_flight_is_instance(flight_dict, flight_instance):
    # check start and end times are the same
    start_at = flight_dict.pop('start_at')
    check_date_time_object_and_str_are_the_same(flight_instance.start_at, start_at)
    end_at = flight_dict.pop('end_at')
    check_date_time_object_and_str_are_the_same(flight_instance.end_at, end_at)

    # check the rest of the fields
    for k, v in flight_dict.items():
        assert getattr(flight_instance, k) == v


def test_can_save_and_retrieve_flights(flight1, flight2, create_flights):
    assert Flight.objects.count() == 2

    saved_flight1 = Flight.objects.get(title='flight 1')
    check_flight_is_instance(flight1, saved_flight1)

    saved_flight2 = Flight.objects.get(title='flight 2')
    check_flight_is_instance(flight2, saved_flight2)
