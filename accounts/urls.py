from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('request/', views.GenerateOTPView.as_view(), name='request-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('email-login/', views.EmailLoginView.as_view(), name='email-login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),

]
