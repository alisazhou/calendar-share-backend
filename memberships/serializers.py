from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Membership


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
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
