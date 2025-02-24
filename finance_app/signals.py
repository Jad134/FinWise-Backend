from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from finance_app.models import Income, Expense, FinancialOverview

@receiver(post_save, sender=Income)
@receiver(post_delete, sender=Income)
@receiver(post_save, sender=Expense)
@receiver(post_delete, sender=Expense)
def update_financial_overview(sender, instance, **kwargs):
    """ Aktualisiert die Gesamtbilanz, wenn Einkommen oder Ausgaben geändert werden. """
    financial_overview, created = FinancialOverview.objects.get_or_create(user=instance.user)
    financial_overview.update_balance()