from django.contrib import admin
from .models import ExchangeRate, FixedAsset, Budget

# Register your models here.
admin.site.register(ExchangeRate)
admin.site.register(FixedAsset)
admin.site.register(Budget)
