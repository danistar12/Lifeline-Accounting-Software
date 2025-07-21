from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PayrollViewSet, PaystubViewSet, TaxViewSet, DeductionViewSet, BenefitViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'payrolls', PayrollViewSet)
router.register(r'paystubs', PaystubViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'deductions', DeductionViewSet)
router.register(r'benefits', BenefitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
