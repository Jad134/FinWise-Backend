from django.urls import path, include
from rest_framework import routers
from user_auth_app.api.views import RegisterView


urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
]