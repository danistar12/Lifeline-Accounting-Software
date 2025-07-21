from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PayrollViewSet, PayrollDeductionViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'payrolls', PayrollViewSet, basename='payroll')
router.register(r'deductions', PayrollDeductionViewSet, basename='payrolldeduction')

urlpatterns = [
    path('', include(router.urls)),
]
