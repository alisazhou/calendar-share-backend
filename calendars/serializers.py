from rest_framework import serializers

from .models import Calendar


class CalendarSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', read_only=True)
    members = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', many=True, read_only=True)

    class Meta:
        model = Calendar
        fields = '__all__'
