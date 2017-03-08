from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Color


class ColorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Color.objects.all(),
                fields=('hex_value', 'calendar'),
                message='Can\'t have repeated colors in the same calendar.'
            )
        ]
