from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/accounting/', include('apps.accounting.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/vendors/', include('apps.vendors.urls')),
    path('api/bills/', include('apps.bills.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/customfields/', include('apps.customfields.urls')),
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/importer/', include('apps.importer.urls')),
    path('api/payroll/', include('apps.payroll.urls')),
    path('api/banking/', include('apps.banking.urls')),
    # Reports and dashboard endpoints
    path('api/reports/', include('apps.reports.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    # Specialized app endpoints
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/budgets/', include('apps.budgets.urls')),
    path('api/taxes/', include('apps.taxes.urls')),
    path('api/invoices/', include('apps.invoices.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
    path('api/assets/', include('apps.assets.urls')),
    # Audit logs
    path('api/audit/', include('apps.audit.urls')),
    path('api/settings/', include('apps.settings.urls')),
    # Swagger/OpenAPI documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
