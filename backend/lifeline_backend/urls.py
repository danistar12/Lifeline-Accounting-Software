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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('apps.accounts.urls')),
    path('accounting/', include('apps.accounting.urls')),
    path('customers/', include('apps.customers.urls')),
    path('vendors/', include('apps.vendors.urls')),
    path('bills/', include('apps.bills.urls')),
    path('payments/', include('apps.payments.urls')),
    path('customfields/', include('apps.customfields.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('documents/', include('apps.documents.urls')),
    path('importer/', include('apps.importer.urls')),
    path('payroll/', include('apps.payroll.urls')),
    path('banking/', include('apps.banking.urls')),
    # Reports and dashboard endpoints
    path('reports/', include('apps.reports.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    # Specialized app endpoints
    path('inventory/', include('apps.inventory.urls')),
    path('projects/', include('apps.projects.urls')),
    path('budgets/', include('apps.budgets.urls')),
    path('taxes/', include('apps.taxes.urls')),
    path('invoices/', include('apps.invoices.urls')),
    path('integrations/', include('apps.integrations.urls')),
    path('assets/', include('apps.assets.urls')),
    # Audit logs
    path('audit/', include('apps.audit.urls')),
    path('settings/', include('apps.settings.urls')),
    # Swagger/OpenAPI documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
