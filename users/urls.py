from .views import CreateUserView , SendVerifyEmailAPI, LoginAPI ,RequestPasswordResetOTPAPI ,VerifyResetPasswordOTPAPI , ChangePasswordAPI
from django.urls import path
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('send-verfiy-opt/', SendVerifyEmailAPI.as_view(), name='send-verfiy-opt'),
    path('login/', LoginAPI.as_view(), name='login-user'),
    path('password-reset-otp/', RequestPasswordResetOTPAPI.as_view(), name='password-reset-otp'),
    path('verify-password-reset-otp/', VerifyResetPasswordOTPAPI.as_view(), name='verify-password-reset-otp'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change-password'),
]