from django.utils import timezone
from datetime import timedelta
from django.db.models import QuerySet

def apply_period_filter(queryset: QuerySet, period: str) -> QuerySet:
    """Wendet einen Zeitraum-Filter (daily, weekly, monthly, yearly) auf ein QuerySet an."""
    today = timezone.now().date()

    if period == "daily":
        return queryset.filter(date=today)
    elif period == "weekly":
        return queryset.filter(date__gte=today - timedelta(days=7))
    elif period == "monthly":
        return queryset.filter(date__month=today.month, date__year=today.year)
    elif period == "yearly":
        return queryset.filter(date__year=today.year)
    
    return queryset
