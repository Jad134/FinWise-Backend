from django.contrib import admin
from .models import Expense
from django.utils.html import format_html
from django.contrib.auth.models import User

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount')  
    list_filter = ('user', 'category')
    search_fields = ('category', 'user__username')


    def changelist_view(self, request, extra_context=None):
        """Zeigt alle Benutzer und ihre Ausgaben an."""
        extra_context = extra_context or {}
        extra_context['title'] = 'Alle Ausgaben nach Benutzer'
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Expense, ExpenseAdmin)
