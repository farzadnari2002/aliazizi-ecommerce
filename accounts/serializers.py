from django.core.validators import RegexValidator
from rest_framework import serializers


class PhoneNumberField(serializers.CharField):
    default_validators = [
        RegexValidator(
            regex=r'^\+?1?\d{9,12}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed."
        )
    ]


class RequestOTP(serializers.ModelSerializer):
    number = PhoneNumberField(max_length=12)


class VerifyOTPRequestSerializer(serializers.Serializer):
    number = PhoneNumberField(max_length=12)
    otp = serializers.IntegerField(required=True)


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
