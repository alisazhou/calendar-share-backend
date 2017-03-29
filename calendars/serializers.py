from rest_framework import serializers

from .models import Calendar
from memberships.models import Membership


class CalendarSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', read_only=True)
    owner_color_hex = serializers.CharField(max_length=6, write_only=True)
    members = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', many=True, read_only=True)

    class Meta:
        model = Calendar
        fields = ('owner', 'owner_color_hex', 'members', 'title', 'url')

    def create(self, validated_data):
        owner_color_hex = validated_data.pop('owner_color_hex')
        owner = validated_data['owner']
        calendar = Calendar.objects.create(**validated_data)
        Membership.objects.create(
            calendar=calendar, member=owner, color_hex=owner_color_hex)
        return calendar
