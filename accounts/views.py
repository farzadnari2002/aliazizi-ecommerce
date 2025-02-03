from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile
from .otp import generate_otp, verify_otp, delete_otp
from .serializers import RequestOTP, VerifyOTPRequestSerializer, EmailLoginSerializer, UpdateUserProfileSerializer


class GenerateOTPView(APIView):
    serializer_class = RequestOTP

    @extend_schema(
        request=RequestOTP,
        responses={
            200: {'description': 'OTP sent successfully'},
            201: {'description': 'User created and OTP sent'},
            400: {'description': 'Invalid request data'}
        },
        summary='Generate OTP for user',
        description="""
        This endpoint generates an OTP for the user based on the provided phone number.
        If the user does not exist, a new user is created.
        """
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user, created = User.objects.get_or_create(number=data['number'])

            otp = generate_otp(user.id)

            print(f'Your OTP is: {otp}')

            return Response(
                data={'message': 'OTP sent successfully'},
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPRequestSerializer

    @extend_schema(
        request=RequestOTP,
        responses={
            200: {'description': 'Login successful', 'examples': {'application/json': {'message': 'Login successful'}}},
            401: {'description': 'Invalid OTP'},
            400: {'description': 'Invalid request data'}
        },
        summary='Login user with OTP verification',
        description="""
        This endpoint verifies the user\'s OTP and logs the user in if the OTP is valid.
         A user must provide their phone number and the OTP received.
         """
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user = get_object_or_404(User, number=data['number'])

            if verify_otp(user.id, data['otp']):
                delete_otp(user.id)
                return Response(data=self._handle_login(data['number']), status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _handle_login(self, number):
        user = User.objects.filter(number=number).first()

        if user is None:
            user = User(number=number)
            user.save()
            created = True
        else:
            created = False

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'created': created
        }


class EmailLoginView(APIView):
    serializer_class = EmailLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user = get_object_or_404(User, email=data['email'])

            if user.check_password(data['password']):
                delete_otp(user.id)
                return Response(data=self._handle_login(data['email']), status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _handle_login(self, email):
        user = User.objects.filter(email=email).first()

        if user is None:
            user = User(email=email)
            user.save()
            created = True
        else:
            created = False

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'created': created
        }


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserProfileSerializer

    def patch(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
