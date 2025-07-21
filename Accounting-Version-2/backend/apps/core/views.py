from django.shortcuts import render
from rest_framework import viewsets

from .models import Company
from .serializers import CompanySerializer
from apps.core.permissions import HasCompanyRole

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['GlobalAdmin']  # Only Global Admins can manage companies

    def get_queryset(self):
        # Global admins can see all companies
        if self.request.user.is_staff:  # A simple way to distinguish global admins
            return Company.objects.all()
        # Other users can only see companies they are associated with
        return self.request.user.companies.all()
