from django.core.validators import RegexValidator
from rest_framework import serializers

from accounts.models import UserProfile


class PhoneNumberField(serializers.CharField):
    default_validators = [
        RegexValidator(
            regex=r'^\+98[0-9]{10}$',
            message="Phone number must be entered in the format: '+9891234567890'. Exactly 12 digits allowed."
        )
    ]


class RequestOTP(serializers.Serializer):
    number = PhoneNumberField(max_length=13)


class VerifyOTPRequestSerializer(serializers.Serializer):
    number = PhoneNumberField(max_length=13)
    otp = serializers.IntegerField(required=True)


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)


class NumberLoginSerializer(serializers.Serializer):
    number = PhoneNumberField(max_length=13)
    password = serializers.CharField(write_only=True)


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True,  min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The two password fields didn't match. Please try again. 🔒")
        return data


class SetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ChangeNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(max_length=13)
