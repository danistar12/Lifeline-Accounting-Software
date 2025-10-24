from rest_framework import viewsets, permissions
from .models import User, Company, UserCompanyRole
from .serializers import UserSerializer, CompanySerializer, UserCompanyRoleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Get or update the current user's information
    """
    user = request.user
    
    if request.method == 'GET':
        # Get user data
        user_data = UserSerializer(user, context={'request': request}).data

        # Get their company roles
        user_company_roles = UserCompanyRole.objects.filter(UserID=user)
        roles_data = UserCompanyRoleSerializer(user_company_roles, many=True).data

        # Combine the data
        response_data = {
            'user': user_data,
            'company_roles': roles_data
        }

        return Response(response_data)
    
    elif request.method == 'PATCH':
        # Update user data
        print(f"PATCH request data: {request.data}")
        print(f"PATCH request files: {request.FILES}")
        
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_user = serializer.save()
            print(f"User updated successfully. Profile photo: {updated_user.profile_photo}")
            
            # Return updated user data with company roles
            user_company_roles = UserCompanyRole.objects.filter(UserID=user)
            roles_data = UserCompanyRoleSerializer(user_company_roles, many=True).data
            
            response_data = {
                'user': UserSerializer(updated_user, context={'request': request}).data,
                'company_roles': roles_data
            }
            
            print(f"Response data: {response_data}")
            return Response(response_data)
        else:
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the companies
        for the currently authenticated user.
        """
        user = self.request.user
        # Correctly filter companies based on the UserCompanyRole intermediate model
        return Company.objects.filter(usercompanyrole__UserID=user)

class UserCompanyRoleViewSet(viewsets.ModelViewSet):
    queryset = UserCompanyRole.objects.all()
    serializer_class = UserCompanyRoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserCompanyRole.objects.filter(UserID=self.request.user)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Get remember_me flag
        remember_me = request.data.get('remember_me', False)
        
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get the tokens from response data
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            # If remember_me, create a new refresh token with longer lifetime
            if remember_me:
                # Create custom refresh token with 30 days lifetime
                refresh = RefreshToken()
                refresh.payload.update({
                    'user_id': request.user.id,
                    'exp': timezone.now() + timedelta(days=30)
                })
                refresh_token = str(refresh)
                
                # Update response data
                response.data['refresh'] = refresh_token
            
            # Set cookies with appropriate settings
            response.set_cookie(
                key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
                value=access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
                value=refresh_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'],
                max_age=30*24*3600 if remember_me else None  # 30 days if remember_me
            )
            
            # Also set session expiry for remember_me
            if remember_me:
                request.session.set_expiry(30 * 24 * 3600)  # 30 days
            else:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                
        return response

class LogoutView(APIView):
    """
    Logout view that doesn't require authentication
    (since logout should work even with invalid/expired tokens)
    """
    permission_classes = []  # No authentication required
    
    def post(self, request, *args, **kwargs):
        response = Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        
        # Try to delete JWT cookies if they exist
        try:
            if hasattr(settings, 'SIMPLE_JWT'):
                response.delete_cookie(settings.SIMPLE_JWT.get('ACCESS_TOKEN_COOKIE', 'access_token'))
                response.delete_cookie(settings.SIMPLE_JWT.get('REFRESH_TOKEN_COOKIE', 'refresh_token'))
        except Exception:
            # If cookie deletion fails, still return success
            pass
            
        return response

def csrf_token(request):
    from django.http import JsonResponse
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_metrics(request):
    """
    Get dashboard financial metrics for the current user's companies
    """
    user = request.user
    companies = Company.objects.filter(usercompanyrole__UserID=user)
    
    # Import here to avoid circular imports
    from apps.accounting.models import GeneralLedger, ChartOfAccount
    
    # Calculate date ranges using timezone-aware datetimes
    now = timezone.localtime()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    current_month_start = today_start.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    current_year_start = today_start.replace(month=1, day=1)
    
    # Get revenue accounts (income/revenue type accounts)
    revenue_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='revenue'
    )
    
    # Get expense accounts
    expense_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='expense'
    )
    
    # Calculate current month revenue
    current_month_revenue = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=revenue_accounts,
        TransactionDate__gte=current_month_start,
        TransactionDate__lt=today_start
    ).aggregate(
        total=Sum('CreditAmount') - Sum('DebitAmount')
    )['total'] or Decimal('0.00')
    
    # Calculate last month revenue for comparison
    last_month_revenue = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=revenue_accounts,
        TransactionDate__gte=last_month_start,
        TransactionDate__lt=current_month_start
    ).aggregate(
        total=Sum('CreditAmount') - Sum('DebitAmount')
    )['total'] or Decimal('0.00')
    
    # Calculate current month expenses
    current_month_expenses = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=expense_accounts,
        TransactionDate__gte=current_month_start,
        TransactionDate__lt=today_start
    ).aggregate(
        total=Sum('DebitAmount') - Sum('CreditAmount')
    )['total'] or Decimal('0.00')
    
    # Calculate last month expenses for comparison
    last_month_expenses = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=expense_accounts,
        TransactionDate__gte=last_month_start,
        TransactionDate__lt=current_month_start
    ).aggregate(
        total=Sum('DebitAmount') - Sum('CreditAmount')
    )['total'] or Decimal('0.00')
    
    # Calculate profit
    current_month_profit = current_month_revenue - current_month_expenses
    last_month_profit = last_month_revenue - last_month_expenses
    
    # Calculate year-to-date cash flow (simplified)
    ytd_cash_flow = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        TransactionDate__gte=current_year_start,
        TransactionDate__lt=today_start
    ).aggregate(
        total=Sum('DebitAmount') - Sum('CreditAmount')
    )['total'] or Decimal('0.00')
    
    # Calculate percentage changes
    def calculate_change(current, previous):
        if previous == 0:
            return 0 if current == 0 else 100
        return float((current - previous) / previous * 100)
    
    revenue_change = calculate_change(current_month_revenue, last_month_revenue)
    expense_change = calculate_change(current_month_expenses, last_month_expenses)
    profit_change = calculate_change(current_month_profit, last_month_profit)
    
    return Response({
        'revenue': {
            'value': float(current_month_revenue),
            'change': revenue_change,
            'label': 'Monthly Revenue'
        },
        'expenses': {
            'value': float(current_month_expenses),
            'change': expense_change,
            'label': 'Monthly Expenses'
        },
        'profit': {
            'value': float(current_month_profit),
            'change': profit_change,
            'label': 'Net Profit'
        },
        'cash_flow': {
            'value': float(ytd_cash_flow),
            'change': 0,  # Would need more complex calculation for cash flow change
            'label': 'YTD Cash Flow'
        }
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_activity(request):
    """
    Get recent activity for dashboard
    """
    user = request.user
    companies = Company.objects.filter(usercompanyrole__UserID=user)
    
    # Import here to avoid circular imports
    from apps.accounting.models import GeneralLedger
    
    # Get recent transactions (last 10)
    recent_transactions = GeneralLedger.objects.filter(
        CompanyID__in=companies
    ).select_related('AccountID').order_by('-CreatedDate')[:10]
    
    activities = []
    for transaction in recent_transactions:
        activity_type = 'income' if transaction.CreditAmount > transaction.DebitAmount else 'expense'
        amount = transaction.CreditAmount if activity_type == 'income' else transaction.DebitAmount

        activities.append({
            'id': transaction.TransactionID,
            'type': activity_type,
            'title': transaction.Description or f'{transaction.AccountID.AccountName} Transaction',
            'details': f'Account: {transaction.AccountID.AccountName}',
            'amount': float(amount),
            'time': transaction.CreatedDate.strftime('%Y-%m-%d %H:%M'),
            'account': transaction.AccountID.AccountName
        })
    
    return Response(activities)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_pending(request):
    """
    Get pending items for dashboard
    """
    user = request.user
    companies = Company.objects.filter(usercompanyrole__UserID=user)
    
    # Import here to avoid circular imports
    from apps.invoices.models import Invoice
    from apps.bills.models import Bill
    
    pending_items = []
    
    # Get pending invoices (this is simplified - you'd need status fields)
    invoices = Invoice.objects.filter(CompanyID__in=companies)[:5]
    for invoice in invoices:
        pending_items.append({
            'id': f'invoice-{invoice.InvoiceID}',
            'type': 'invoice',
            'title': f'Invoice #{invoice.InvoiceNumber}',
            'subtitle': f'Customer: {invoice.CustomerID.Name}',
            'urgent': True  # Simplified - would check due dates
        })
    
    # Get pending bills
    bills = Bill.objects.filter(CompanyID__in=companies)[:5]
    for bill in bills:
        pending_items.append({
            'id': f'bill-{bill.BillID}',
            'type': 'bill',
            'title': f'Bill #{bill.BillNumber}',
            'subtitle': f'Vendor: {bill.VendorID.Name}',
            'urgent': False
        })
    
    return Response(pending_items)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_financial_health(request):
    """
    Calculate financial health score and metrics
    """
    user = request.user
    companies = Company.objects.filter(usercompanyrole__UserID=user)
    
    # Import here to avoid circular imports
    from apps.accounting.models import GeneralLedger, ChartOfAccount
    
    # Calculate various financial health indicators
    now = timezone.localtime()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_year_start = current_month_start.replace(month=1, day=1)
    
    # Get account types
    revenue_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='revenue'
    )
    expense_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='expense'
    )
    asset_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='asset'
    )
    liability_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='liability'
    )
    
    # Calculate metrics
    total_revenue = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=revenue_accounts,
        TransactionDate__gte=current_year_start
    ).aggregate(total=Sum('CreditAmount'))['total'] or Decimal('0.00')
    
    total_expenses = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=expense_accounts,
        TransactionDate__gte=current_year_start
    ).aggregate(total=Sum('DebitAmount'))['total'] or Decimal('0.00')
    
    total_assets = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=asset_accounts
    ).aggregate(total=Sum('DebitAmount') - Sum('CreditAmount'))['total'] or Decimal('0.00')
    
    total_liabilities = GeneralLedger.objects.filter(
        CompanyID__in=companies,
        AccountID__in=liability_accounts
    ).aggregate(total=Sum('CreditAmount') - Sum('DebitAmount'))['total'] or Decimal('0.00')
    
    # Calculate health score (simplified algorithm)
    profit_margin = float((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else 0
    debt_to_asset_ratio = float(total_liabilities / total_assets * 100) if total_assets > 0 else 0
    
    # Simple scoring algorithm
    score = 85  # Base score
    
    if profit_margin > 20:
        score += 10
    elif profit_margin > 10:
        score += 5
    elif profit_margin < 0:
        score -= 20
    
    if debt_to_asset_ratio < 30:
        score += 5
    elif debt_to_asset_ratio > 70:
        score -= 15
    
    score = max(0, min(100, score))  # Keep between 0-100
    
    # Determine health status
    if score >= 80:
        status = 'excellent'
    elif score >= 65:
        status = 'good'
    elif score >= 50:
        status = 'fair'
    else:
        status = 'poor'
    
    return Response({
        'score': score,
        'status': status,
        'metrics': {
            'profit_margin': round(profit_margin, 1),
            'debt_ratio': round(debt_to_asset_ratio, 1),
            'cash_position': float(total_assets - total_liabilities),
            'revenue_growth': 12.5  # Placeholder - would need historical data
        }
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_charts(request):
    """
    Get chart data for dashboard
    """
    user = request.user
    companies = Company.objects.filter(usercompanyrole__UserID=user)
    
    # Import here to avoid circular imports
    from apps.accounting.models import GeneralLedger, ChartOfAccount
    
    # Get last 6 months of revenue data
    reference_month_start = timezone.localtime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    revenue_data = []
    
    for i in range(6):
        month_start = (reference_month_start - timedelta(days=i * 30)).replace(day=1)
        next_month_start = (month_start + timedelta(days=32)).replace(day=1)
        
        revenue_accounts = ChartOfAccount.objects.filter(
            CompanyID__in=companies,
            AccountType__icontains='revenue'
        )
        
        month_revenue = GeneralLedger.objects.filter(
            CompanyID__in=companies,
            AccountID__in=revenue_accounts,
            TransactionDate__gte=month_start,
            TransactionDate__lt=next_month_start
        ).aggregate(
            total=Sum('CreditAmount') - Sum('DebitAmount')
        )['total'] or Decimal('0.00')
        
        revenue_data.insert(0, {
            'month': month_start.strftime('%b'),
            'value': float(month_revenue)
        })
    
    # Get expense breakdown by account type
    expense_accounts = ChartOfAccount.objects.filter(
        CompanyID__in=companies,
        AccountType__icontains='expense'
    )
    
    expense_breakdown = []
    for account in expense_accounts[:5]:  # Top 5 expense accounts
        total = GeneralLedger.objects.filter(
            CompanyID__in=companies,
            AccountID=account,
            TransactionDate__gte=reference_month_start
        ).aggregate(
            total=Sum('DebitAmount') - Sum('CreditAmount')
        )['total'] or Decimal('0.00')

        if total > 0:
            expense_breakdown.append({
                'label': account.AccountName,
                'value': float(total),
                'color': f'#{"".join([f"{hash(account.AccountName) % 16:x}" for _ in range(6)])}'[:7]
            })
    
    return Response({
        'revenue_trend': revenue_data,
        'expense_breakdown': expense_breakdown
    })
