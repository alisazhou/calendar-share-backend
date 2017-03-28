from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Flight, Plan
from calendars.models import Calendar


User = get_user_model()


class CalendarPostField(serializers.HyperlinkedRelatedField):
    """
    Custom related field so that the queryset can be generated dynamically
    based on currently logged-in user. A user should only be able to add
    flights to calendars that they are members of. Accordingly, the choices
    in Calendar field are limited to those.
    """
    def get_queryset(self):
        curr_user = self.context['request'].user
        if curr_user.is_staff:
            return Calendar.objects.all()
        else:
            return curr_user.calendars_shared.all()


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    calendar = CalendarPostField(view_name='calendar-detail')
    owner = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only='true')

    class Meta:
        model = Flight
        fields = (
            'title', 'owner', 'calendar', 'start_at', 'end_at', 'confirmed',
            'notes', 'departure', 'arrival', 'airline', 'flight_no', 'url')

    def validate(self, data):
        if data.get('start_at', 0) > data.get('end_at', 1):
            raise serializers.ValidationError('End time must come after start.')
        if data.get('confirmed') is True:
            # if confirmed, must provide airline and flight no
            if not (data.get('airline') or getattr(self.instance, 'airline', False)):
                raise serializers.ValidationError('Airline is required')
            if not (data.get('flight_no') or getattr(self.instance, 'flight_no', False)):
                raise serializers.ValidationError('Flight number is required')

        # .validate() method must return validated data
        return data


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only='true')

    class Meta:
        model = Plan
        fields = (
            'title', 'owner', 'calendar', 'start_at', 'end_at', 'confirmed',
            'notes', 'location', 'url')

    def validate(self, data):
        # if current post/patch data has event time
        if data.get('start_at', 0) > data.get('end_at', 1):
            raise serializers.ValidationError('End time must come after start.')
        return data
