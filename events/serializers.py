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
