from rest_framework import serializers
from accounts.models import UserProfile


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']


class SetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
