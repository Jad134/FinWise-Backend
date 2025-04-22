from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import CustomUser
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save() 
            token, created = Token.objects.get_or_create(user=user)  
            
            return Response(
                {
                    "message": "Benutzer erfolgreich registriert.",
                    "token": token.key
                }, 
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomAuthToken(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")


        error_response = self.check_credentials(username, password)
        if error_response:
            return error_response
        
        user = self.check_user_password(username, password)
        if user is None:
            return Response(
                {"error": "Falsches Passwort oder Benutzer existiert nicht"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
    def check_credentials(self, username, password):
        """Überprüft, ob Benutzername und Passwort vorhanden sind."""
        if not username or not password:
            return Response(
                {"error": "Benutzername und Passwort erforderlich"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None    

    def check_user_password(self, username, password):
        """Überprüft Benutzerexistenz und Passwort und gibt den Benutzer zurück."""
        user = authenticate(username=username, password=password)
        if user is None:
            
            if not CustomUser.objects.filter(username=username).exists():
                return None 
        return user
