from rest_framework import serializers

from .models import Flight, Plan
from calendars.models import Calendar
from profiles.models import Profile



class FlightSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only='true')

    class Meta:
        model = Flight
        fields = '__all__'

    def validate(self, data):
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError('End time must come after start.')
        elif data['confirmed'] == True:
            if not data['airline']:
                raise serializers.ValidationError('Airline is required')
            if not data['flight_no']:
                raise serializers.ValidationError('Flight number is required')



class PlanSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only='true')

    class Meta:
        model = Plan
        fields = '__all__'

    def validate(self, data):
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError('End time must come after start.')
        return data
