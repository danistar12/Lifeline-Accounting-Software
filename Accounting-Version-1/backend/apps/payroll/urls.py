from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PayrollViewSet, PayrollDeductionViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'payrolls', PayrollViewSet)
router.register(r'deductions', PayrollDeductionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
