from rest_framework import serializers
from .auth_serializers import PhoneNumberField
import re


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(required=True, write_only=True, min_length=8, *args, **kwargs)

        def validate(self, value):
            # Validate password length
            if len(value) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long.")
            
            # Validate password contains a uppercase letter
            if not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter.")
            
            # Validate password contains a lowercase letter
            if not re.search(r'[a-z]', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter.")
            
            # Validate password contains a number
            if not re.search(r'[0-9]', value):
                raise serializers.ValidationError("Password must contain at least one number.")
            
            # Validate password contains a special character
            if not re.search(r'[!@#$%^&*()_+{}":;\']', value):
                raise serializers.ValidationError("Password must contain at least one special character.")


class PhoneEmailBaseSerializer(serializers.Serializer):
    number = PhoneNumberField(max_length=13, required=False)
    email = serializers.EmailField(required=False)

    # Validate phone number or email
    def validate(self, attrs):
        number = attrs.get('number', None)
        email = attrs.get('email', None)

        if not number and not email or number and email:
            raise serializers.ValidationError("Please provide either a phone number or an email address.")

        return attrs


class BasePasswordSerializer(serializers.Serializer):
    password = PasswordField()
    confirm_password = PasswordField()
    
    # Validate password match
    def validate(self, attrs):
        super().validate(attrs)


        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("The two password fields didn't match. Please try again. 🔒")
        return attrs


class ForgotPasswordRequestSerializer(PhoneEmailBaseSerializer):
    pass
    

class ForgotPasswordVerifySerializer(PhoneEmailBaseSerializer, BasePasswordSerializer):
    otp = serializers.IntegerField(required=True)


class ChangePasswordSerializer(BasePasswordSerializer):
    old_password = serializers.CharField(write_only=True)
