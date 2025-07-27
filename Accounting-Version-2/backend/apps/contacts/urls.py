from rest_framework import routers
from .views import CustomerViewSet, VendorViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'vendors', VendorViewSet, basename='vendor')

urlpatterns = router.urls
