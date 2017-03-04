from rest_framework import serializers

from .models import Event
from calendars.models import Calendar
from profiles.models import Profile


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only='true')

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError('End time must come after start.')
        return data
