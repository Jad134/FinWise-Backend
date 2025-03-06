from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Income(models.Model):
    user = models.ForeignKey(User, related_name='incomes', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Income of {self.amount} from {self.source}"

class Expense(models.Model):
    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Expense of {self.amount} for {self.category} from {self.user}"


class FinancialOverview(models.Model):
    """ Speichert das aktuelle Finanzziel des Benutzers und die Gesamtbilanz """
    user = models.OneToOneField(User, related_name='financial_overview', on_delete=models.CASCADE)
    target_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def calculate_total_income(self):
        """ Berechnet das gesamte Einkommen des Nutzers """
        return self.user.incomes.aggregate(total=models.Sum('amount'))['total'] or 0

    def calculate_total_expenses(self):
        """ Berechnet die gesamten Ausgaben des Nutzers """
        return self.user.expenses.aggregate(total=models.Sum('amount'))['total'] or 0

    def update_balance(self):
        """ Aktualisiert die Gesamtbilanz """
        self.total_balance = self.calculate_total_income() - self.calculate_total_expenses()
        self.save()

    def __str__(self):
        return f"Financial Overview for {self.user.username} - Balance: {self.total_balance}"