from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Membership
from calendars.models import Calendar


User = get_user_model()


class CalendarPostField(serializers.HyperlinkedRelatedField):
    """
    Custom related field so that the queryset can be generated dynamically
    based on currently logged-in user. A user should only be able to add
    members to calendars that they are the owner of. Accordingly, the choices
    in Calendar field are limited to those.
    """
    def get_queryset(self):
        curr_user = self.context['request'].user
        if curr_user.is_staff:
            return Calendar.objects.all()
        else:
            return curr_user.calendars_owned.all()


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    calendar = CalendarPostField(view_name='calendar-detail')
    member = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', queryset=User.objects.all())

    class Meta:
        model = Membership
        fields = ('calendar', 'member', 'color_hex')
        validators = [
            UniqueTogetherValidator(
                queryset=Membership.objects.all(),
                fields=('color_hex', 'calendar'),
                message='Members cannot have the same color.'
            )
        ]
