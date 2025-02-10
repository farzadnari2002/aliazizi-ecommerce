from rest_framework import serializers
from accounts.models import UserProfile, User


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']


class SetEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',]
