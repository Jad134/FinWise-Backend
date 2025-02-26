from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, ExpenseViewSet, FinancialOverviewViewSet


router = DefaultRouter()
router.register(r'income', IncomeViewSet, basename='income')
router.register(r'expense', ExpenseViewSet, basename='expense')
router.register(r'overview', FinancialOverviewViewSet, basename='overview')

urlpatterns = [
    path('', include(router.urls)),
]