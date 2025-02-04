from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    date_of_birth = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'date_of_birth', 'password', 'confirm_password']

    def validate_email(self, value):
        """ Überprüft, ob die E-Mail bereits existiert """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Diese E-Mail-Adresse wird bereits verwendet.")
        return value

    def validate(self, data):
        """ Überprüft, ob die Passwörter übereinstimmen """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwörter stimmen nicht überein."})
        return data

    def create(self, validated_data):
        """ Erstellt den Benutzer, entfernt confirm_password und gibt ihn zurück """
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate_date_of_birth(self, value):
        """ Konvertiert dd/mm/yyyy zu einem echten Datumsobjekt """
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            raise serializers.ValidationError("Ungültiges Datum. Bitte im Format TT/MM/JJJJ eingeben.")