from .views import CreateUserView , SendVerifyEmailAPI, LoginAPI
from django.urls import path
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('send-verfiy-opt/', SendVerifyEmailAPI.as_view(), name='send-verfiy-opt'),
    path('login/', LoginAPI.as_view(), name='login-user'),
]