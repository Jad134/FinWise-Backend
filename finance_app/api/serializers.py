from rest_framework import serializers
from finance_app.models import Income, Expense, FinancialOverview

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class FinancialOverviewSerializer(serializers.ModelSerializer):
    total_income = serializers.SerializerMethodField()
    total_expenses = serializers.SerializerMethodField()

    class Meta:
        model = FinancialOverview
        fields = ['user', 'target_savings', 'total_balance', 'total_income', 'total_expenses']

    def get_total_income(self, obj):
        return obj.calculate_total_income()

    def get_total_expenses(self, obj):
        return obj.calculate_total_expenses()
