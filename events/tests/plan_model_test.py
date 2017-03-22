from events.models import Plan
from events.tests.event_plugins import check_event_is_instance


def test_can_save_and_retrieve_plans(plan1, plan2, create_plans):
    assert Plan.objects.count() == 2

    saved_plan1 = Plan.objects.get(title='plan 1')
    check_event_is_instance(plan1, saved_plan1)

    saved_plan2 = Plan.objects.get(title='plan 2')
    check_event_is_instance(plan2, saved_plan2)
