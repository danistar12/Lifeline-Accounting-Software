from rest_framework import routers
from .views import CustomerViewSet, VendorViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'vendors', VendorViewSet)

urlpatterns = router.urls
