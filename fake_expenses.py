import os
import django

# Django Umgebung initialisieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinWise.settings')  # Ersetze 'dein_projekt' mit deinem Projektnamen
django.setup()

from django.utils import timezone
import random
from finance_app.models import Expense
from django.contrib.auth import get_user_model

# Benutzer abrufen
USER_ID = 1
User = get_user_model()
user = User.objects.get(id=USER_ID)

# Kategorien
CATEGORIES = ["food", "groceries", "transport", "entertainment"]
DESCRIPTIONS = {
    "food": ["McDonald's", "Burger King", "Subway", "KFC", "Dönerladen"],
    "groceries": ["Edeka", "Aldi", "Lidl", "Rewe", "Kaufland"],
    "transport": ["Bus Ticket", "Bahn Ticket", "Tankstelle", "Taxi", "E-Scooter"],
    "entertainment": ["Kino", "Netflix", "Spotify", "Freizeitpark", "Theater"]
}

today = timezone.now().date()
expenses = []

for month_offset in range(1, 5):
    for _ in range(5):
        category = random.choice(CATEGORIES)
        description = random.choice(DESCRIPTIONS[category])
        amount = round(random.uniform(5, 200), 2)
        date = today.replace(day=random.randint(1, 28)) - timezone.timedelta(days=month_offset * 30)

        expenses.append(Expense(user=user, category=category, description=description, amount=amount, date=date))

Expense.objects.bulk_create(expenses)

print(f"{len(expenses)} Fake-Expenses erfolgreich erstellt!")
