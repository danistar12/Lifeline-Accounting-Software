from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PayrollViewSet, PayrollDeductionViewSet, PayStubViewSet, TaxViewSet, BenefitViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'payrolls', PayrollViewSet)
router.register(r'deductions', PayrollDeductionViewSet)
router.register(r'paystubs', PayStubViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'benefits', BenefitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
