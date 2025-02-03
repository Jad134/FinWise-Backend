from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

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