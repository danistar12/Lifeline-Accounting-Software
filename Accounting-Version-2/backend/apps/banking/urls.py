from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet, BankTransactionViewSet

router = DefaultRouter()
router.register(r'accounts', BankAccountViewSet)
router.register(r'transactions', BankTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
