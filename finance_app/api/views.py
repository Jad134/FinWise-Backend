from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from finance_app.api.pagination import ExpensePagination
from finance_app.models import Income, Expense, FinancialOverview
from .serializers import IncomeSerializer, ExpenseSerializer, FinancialOverviewSerializer
from rest_framework.permissions import IsAuthenticated
from .filters import apply_period_filter
from django.db.models import Sum
from django.utils.timezone import now



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


class LazyLoadExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    pagination_class = ExpensePagination  

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')




class FinancialOverviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        overview, created = FinancialOverview.objects.get_or_create(user=request.user)
        serializer = FinancialOverviewSerializer(overview)
        return Response(serializer.data)

    
class TopCategoriesView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer



    def list(self, request): 
         top_categories = FilterTopCategories.get_top_categories_for_user(request.user)
         return Response(top_categories)


class FilterTopCategories():
     
     @staticmethod
     def get_top_categories_for_user(user):
         today = now()
         try:
             top_categories = Expense.objects.filter(
                 user=user,
                 date__month=today.month,  
                 date__year=today.year      
             ).values('category') \
             .annotate(total_amount=Sum('amount')) \
             .order_by('-total_amount')[:2]
             return top_categories
         except Expense.DoesNotExist:
             return[]
         except Exception as e:
             print('Fehler beim Aufrufen der Top-Categorien', e)
             return[]
             
     
     

    
    
