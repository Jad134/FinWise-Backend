from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Benutzer speichern
            token, created = Token.objects.get_or_create(user=user)  # Token erstellen oder abrufen
            
            return Response(
                {
                    "message": "Benutzer erfolgreich registriert.",
                    "token": token.key
                }, 
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomAuthToken(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Benutzername und Passwort erforderlich"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is None:
            if not User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Benutzer existiert nicht"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Falsches Passwort"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)