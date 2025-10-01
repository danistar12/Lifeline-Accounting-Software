from rest_framework import serializers

class ReportPeriodSerializer(serializers.Serializer):
    """Serializer for report period filtering"""
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    
    def validate(self, data):
        """
        Check that start_date is before end_date
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class FinancialReportItemSerializer(serializers.Serializer):
    """Serializer for financial report line items"""
    account_type = serializers.CharField()
    account_name = serializers.CharField()
    balance = serializers.DecimalField(max_digits=18, decimal_places=2)

class BalanceSheetSerializer(serializers.Serializer):
    """Serializer for balance sheet data"""
    assets = FinancialReportItemSerializer(many=True)
    liabilities = FinancialReportItemSerializer(many=True)
    equity = FinancialReportItemSerializer(many=True)
    total_assets = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_liabilities = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_equity = serializers.DecimalField(max_digits=18, decimal_places=2)

class IncomeStatementSerializer(serializers.Serializer):
    """Serializer for income statement data"""
    revenue = FinancialReportItemSerializer(many=True)
    expenses = FinancialReportItemSerializer(many=True)
    total_revenue = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=18, decimal_places=2)
    net_income = serializers.DecimalField(max_digits=18, decimal_places=2)

class CashFlowSerializer(serializers.Serializer):
    """Serializer for cash flow statement data"""
    operating_activities = FinancialReportItemSerializer(many=True)
    investing_activities = FinancialReportItemSerializer(many=True)
    financing_activities = FinancialReportItemSerializer(many=True)
    net_cash_change = serializers.DecimalField(max_digits=18, decimal_places=2)
    beginning_cash_balance = serializers.DecimalField(max_digits=18, decimal_places=2)
    ending_cash_balance = serializers.DecimalField(max_digits=18, decimal_places=2)
