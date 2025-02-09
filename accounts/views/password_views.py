from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from accounts.serializers.password_serializers import *
from accounts.otp import *



class SetNewPasswordRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetNewPasswordRequestSerializer

    def post(self, request):
        user=request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            new_number = data.get('number')
            new_email = data.get('email')

            if new_number:

                if user.number != data['number']:
                    otp = generate_otp_pass
                    print(f'Your OTP is: {otp}')

                    return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)
                return Response({"detail": "New number must be different from the current number."}, status=status.HTTP_400_BAD_REQUEST)
            
            if new_email:
                
                if user.email != data['email']:
                    otp = generate_otp_pass
                    print(f'Your OTP is: {otp}')
                    #todo : send email

                    return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)
                return Response({"detail": "New email must be different from the current email."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetNewPasswordVerifySerializer

    def post(self, request):
        user=request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            new_password = data['new_password']
            otp = data['otp']

            if verify_otp_pass(user.id, otp):
                user.set_password(new_password)
                user.save()
                delete_otp_pass(user.id)
                return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.Serializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid():
            data = serializer.validated_data
            old_password = data['old_password']
            new_password = data['new_password']

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
