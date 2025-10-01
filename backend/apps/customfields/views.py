from rest_framework import viewsets
from .models import CustomField, CustomFieldValue
from .serializers import CustomFieldSerializer, CustomFieldValueSerializer

class CustomFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer

    def get_queryset(self):
        """
        Filter custom fields by user's companies
        """
        user = self.request.user
        return CustomField.objects.filter(CompanyID__usercompanyrole__UserID=user)

class CustomFieldValueViewSet(viewsets.ModelViewSet):
    queryset = CustomFieldValue.objects.all()
    serializer_class = CustomFieldValueSerializer
