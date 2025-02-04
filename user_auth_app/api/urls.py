from django.urls import path, include
from rest_framework import routers
from user_auth_app.api.views import CustomAuthToken, RegisterView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
]