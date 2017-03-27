from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Membership


User = get_user_model()


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
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
