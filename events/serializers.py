from rest_framework import serializers

from .models import Flight, Plan


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only='true')

    class Meta:
        model = Flight
        fields = (
            'title', 'owner', 'calendar', 'start_at', 'end_at', 'confirmed',
            'notes', 'departure', 'arrival', 'airline', 'flight_no')

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
        fields = '__all__'

    def validate(self, data):
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError('End time must come after start.')
        return data
