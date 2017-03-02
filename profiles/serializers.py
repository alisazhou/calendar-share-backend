from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(
        source='user.password',
        min_length=6,
        write_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')


    class Meta:
        model = Profile
        fields = ('id', 'username', 'email', 'password', 'first_name',
            'last_name', 'bday', 'phone', 'url')


    def create(self, validated_data):
        user_data = validated_data['user']
        user = User(**user_data)
        user.set_password(user_data['password'])
        user.save()

        profile = Profile(
            bday=validated_data['bday'],
            phone=validated_data['phone'])
        profile.user = user
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
