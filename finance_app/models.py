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
        return f"Expense of {self.amount} for {self.category}"

