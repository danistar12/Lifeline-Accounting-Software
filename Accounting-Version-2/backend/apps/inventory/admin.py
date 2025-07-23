from django.contrib import admin
from .models import Inventory, InventoryLocation

# Register your models here.
admin.site.register(Inventory)
admin.site.register(InventoryLocation)
