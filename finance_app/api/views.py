from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from finance_app.models import Income, Expense, FinancialOverview
from .serializers import IncomeSerializer, ExpenseSerializer, FinancialOverviewSerializer
from rest_framework.permissions import IsAuthenticated
from .filters import apply_period_filter
from django.db.models import Sum
from django.utils.timezone import now


# ✅ Income ViewSet
class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        queryset = Income.objects.filter(user=self.request.user)
        period = self.request.query_params.get("period", None)
        if period:
            queryset = apply_period_filter(queryset, period)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ Expense ViewSet
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)

        category_filter = self.request.query_params.get("filter", None)
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        period = self.request.query_params.get("period", None)
        if period:
            queryset = apply_period_filter(queryset, period)

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


class TopCategoriesView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        today = now()
        top_categories = Expense.objects.filter(
            user=request.user,
            date__month=today.month,  
            date__year=today.year      
        ).values('category') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('-total_amount')[:2]  

        return Response(top_categories)