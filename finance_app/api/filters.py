from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db.models import QuerySet

def apply_period_filter(queryset: QuerySet, period: str) -> QuerySet:
    """Applies a time period filter (daily, weekly, monthly, yearly) to a QuerySet."""
    today = timezone.now().date()

    if period == "daily":
        return queryset.filter(date=today)
    elif period == "weekly":
        return queryset.filter(date__gte=today - timedelta(days=7))
    elif period == "monthly":
        return queryset.filter(date__month=today.month, date__year=today.year)
    elif period == "yearly":
        return queryset.filter(date__year=today.year)
    
    raise ValidationError({"period": "Invalid period value. Must be one of: daily, weekly, monthly, yearly."})
