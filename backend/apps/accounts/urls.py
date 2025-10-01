from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, UserCompanyRoleViewSet, LoginView, LogoutView, csrf_token, current_user,
    dashboard_metrics, dashboard_activity, dashboard_pending, dashboard_financial_health, dashboard_charts
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'user-company-roles', UserCompanyRoleViewSet, basename='usercompanyrole')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/csrf/', csrf_token, name='csrf'),
    path('auth/user/', current_user, name='current_user'),
    path('dashboard/metrics/', dashboard_metrics, name='dashboard_metrics'),
    path('dashboard/activity/', dashboard_activity, name='dashboard_activity'),
    path('dashboard/pending/', dashboard_pending, name='dashboard_pending'),
    path('dashboard/health/', dashboard_financial_health, name='dashboard_health'),
    path('dashboard/charts/', dashboard_charts, name='dashboard_charts'),
    path('', include(router.urls)),
]
