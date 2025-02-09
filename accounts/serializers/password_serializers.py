from rest_framework import serializers
from .auth_serializers import PhoneNumberField


class SetNewPasswordRequestSerializer(serializers.Serializer):
    number = PhoneNumberField(max_length=13, required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        number = attrs.get('number', None)
        email = attrs.get('email', None)

        if not number and not email or number and email:
            raise serializers.ValidationError("Please provide either a phone number or an email address.")

        return attrs


class SetNewPasswordVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True,  min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The two password fields didn't match. Please try again. 🔒")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The two password fields didn't match. Please try again.")
        return data
