from datetime import date
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from finance_app.models import Income

User = get_user_model()


class IncomeViewTest(APITestCase):

    def setUp(self):
        """Create an real user and token, wich is temporary for tests."""
        self.client = APIClient()

        self.test_user = User.objects.create_user(
            username='jadss', 
            password='das',
            date_of_birth=date(1990, 1, 1),
            mobile_number='22222',
            email='dd@we.de'
        )

        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.income = Income.objects.create(
            user = self.test_user,
            amount = 200,
            source = 'rent',
            date = "2024-04-01"
        )

    def test_get_income(self):
        url = reverse('income-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_detail_income(self):
        url = reverse('income-detail', kwargs={'pk': self.income.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["source"], "rent")




    