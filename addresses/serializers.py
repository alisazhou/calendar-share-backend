from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='profile-detail', read_only=True)

    class Meta:
        model = Address
        fields = ('url', 'street', 'city', 'state', 'zipcode', 'user')
