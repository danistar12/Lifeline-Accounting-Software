"""
URL configuration for lifeline_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('apps.core.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/payroll/', include('apps.payroll.urls')),
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/banking/', include('apps.banking.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/payments-ap/', include('apps.payments_ap.urls')),
    path('api/payments-ar/', include('apps.payments_ar.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
]
