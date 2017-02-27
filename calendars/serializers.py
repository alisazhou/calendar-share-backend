from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Calendar


class CalendarSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail', queryset=User.objects.all())
    members = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=User.objects.all())

    class Meta:
        model = Calendar
        fields = '__all__'
