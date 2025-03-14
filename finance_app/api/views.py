from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from finance_app.models import Income, Expense, FinancialOverview
from .serializers import IncomeSerializer, ExpenseSerializer, FinancialOverviewSerializer
from rest_framework.permissions import IsAuthenticated

# ✅ Income ViewSet
class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        period = self.request.query_params.get('period', None)
        if period:
            today = timezone.now().date()
            if period == "daily":
                queryset = queryset.filter(date=today)
            elif period == "weekly":
                queryset = queryset.filter(date__gte=today - timedelta(days=7))
            elif period == "monthly":
                queryset = queryset.filter(date__month=today.month, date__year=today.year)
            elif period == "yearly":
                queryset = queryset.filter(date__year=today.year)

        return queryset

# ✅ Expense ViewSet
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user) 

        category_filter = self.request.query_params.get('filter', None)
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        period = self.request.query_params.get('period', None)
        if period:
            today = timezone.now().date()
            if period == "daily":
                queryset = queryset.filter(date=today)
            elif period == "weekly":
                queryset = queryset.filter(date__gte=today - timedelta(days=7))
            elif period == "monthly":
                queryset = queryset.filter(date__month=today.month, date__year=today.year)
            elif period == "yearly":
                queryset = queryset.filter(date__year=today.year)

        return queryset  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  


# ✅ Financial Overview ViewSet (Nur Read-Only)
class FinancialOverviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        overview, created = FinancialOverview.objects.get_or_create(user=request.user)
        serializer = FinancialOverviewSerializer(overview)
        return Response(serializer.data)
