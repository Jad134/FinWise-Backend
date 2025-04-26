from django.contrib import admin
from .models import Expense, FinancialOverview, Income
from django.utils.html import format_html
from django.contrib.auth.models import User

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount')  
    list_filter = ('user', 'category')
    search_fields = ('category', 'user__username')


    def changelist_view(self, request, extra_context=None):
        """Shows all users and their expenses."""
        extra_context = extra_context or {}
        extra_context['title'] = 'Alle Ausgaben nach Benutzer'
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Expense, ExpenseAdmin)

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'amount')  
    list_filter = ('user', 'source')
    search_fields = ('source', 'user__username')

    def changelist_view(self, request, extra_context=None):
        """Shows all users and their income."""
        extra_context = extra_context or {}
        extra_context['title'] = 'Alle Einkommen nach Benutzer'
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Income, IncomeAdmin) 

class OverviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_savings', 'total_balance')  
    list_filter = ('user',)
    search_fields = ('user__username',)

    def changelist_view(self, request, extra_context=None):
        """Displays all users and their financial overview"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Alle Finanzübersichten nach Benutzer'
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(FinancialOverview, OverviewAdmin)

