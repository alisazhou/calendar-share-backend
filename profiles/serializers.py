from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile
from addresses.models import Address


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(
        source='user.password',
        min_length=6,
        write_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    street = serializers.CharField(required=False, source='address.street')
    city = serializers.CharField(required=False, source='address.city')
    state = serializers.CharField(required=False, source='address.state')
    zipcode = serializers.CharField(required=False, source='address.zipcode')

    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'bday', 'phone', 'street', 'city', 'state', 'zipcode', 'url', )

    def create(self, validated_data):
        profile = Profile(
            bday=validated_data.get('bday'),
            phone=validated_data.get('phone'))

        user_data = validated_data['user']
        user = User(**user_data)
        user.set_password(user_data['password'])
        user.save()
        profile.user = user

        address_data = validated_data.get('address')
        if address_data:
            address = Address.objects.create(**address_data)
            profile.address = address

        profile.save()

        return profile

    def update(self, instance, validated_data):
        user = instance.user
        for attr, value in validated_data.get('user', {}).items():
            setattr(user, attr, value)
        user.save()

        profile = instance
        profile.bday = validated_data.get('bday', profile.bday)
        profile.phone = validated_data.get('phone', profile.phone)
        profile.save()

        return profile
