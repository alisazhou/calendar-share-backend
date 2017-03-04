from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Calendar
from profiles.models import Profile


User = get_user_model()

class CalendarSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True)
    members = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', many=True, queryset=Profile.objects.all())

    class Meta:
        model = Calendar
        fields = '__all__'
