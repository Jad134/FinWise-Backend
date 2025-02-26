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

# ✅ Expense ViewSet
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ✅ Financial Overview ViewSet (Nur Read-Only)
class FinancialOverviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        overview, created = FinancialOverview.objects.get_or_create(user=request.user)
        serializer = FinancialOverviewSerializer(overview)
        return Response(serializer.data)
