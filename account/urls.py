from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='user-register'),
    path('verify-account/', VerifyAccountAPI.as_view(), name='verify_account'),
    path('verify-account-sms/', VerifyPhoneNumber.as_view(), name='verify_account_sms'),
    path('2fa/enable/', EnableTwoFactorAuthView.as_view(), name='enable-2fa'),
    path('2fa/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    # path('verify-kyc-enable/', KycEnableView.as_view(), name='kyc-enabled-request'),
    path('login/', LoginAPI.as_view(), name='user-login'),
    path('admin/login/', AdminLoginAPI.as_view(), name='admin-user-login'),
    path('verify-login/', TwoFactorAuthVerificationAPI.as_view(), name='verify_login'),
    path('user/2fa/', TwoFactorAuthAPI.as_view(), name='two_factor_auth'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('users/', UserListViewAPI.as_view(), name='user-list'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('change-password/', ChangePassword.as_view(), name='password_change'),
    path('reset-password-email/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password-phone/', PasswordResetPhoneView.as_view(), name='password_reset'),
    path('reset-password/confirm-email/', PasswordResetConfirmationView.as_view(), name='password_reset_confirm'),
    path('reset-password/confirm-phone/', PasswordResetConfirmationPhoneView.as_view(), name='password_reset_confirm'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),

    path('pin/', CreatPinView.as_view(), name="pin"),
    path('pin-compare/', ComparePin.as_view(),name="pin-compare"),
    path('pin-change/', ChangePin.as_view(),name="pin-change"),

    path('kyc/', UpdateKYCStatus.as_view(), name="kyc"),
    path('user/', UserView.as_view(), name='user'),
]