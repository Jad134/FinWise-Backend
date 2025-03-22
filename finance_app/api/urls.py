from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, ExpenseViewSet, FinancialOverviewViewSet, LazyLoadExpenseViewSet, TopCategoriesView


router = DefaultRouter()
router.register(r'income', IncomeViewSet, basename='income')
router.register(r'expense', ExpenseViewSet, basename='expense')
router.register(r'overview', FinancialOverviewViewSet, basename='overview')
router.register(r'top-categories', TopCategoriesView, basename='top-categories')
router.register(r'latest-expenses', LazyLoadExpenseViewSet, basename='lazy-loading-expense')

urlpatterns = [
    path('', include(router.urls)),
]