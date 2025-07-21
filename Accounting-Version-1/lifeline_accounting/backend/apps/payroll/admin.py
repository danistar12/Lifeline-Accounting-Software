from django.contrib import admin
from .models import Employee, Payroll, Paystub, Tax, Deduction, Benefit

admin.site.register(Employee)
admin.site.register(Payroll)
admin.site.register(Paystub)
admin.site.register(Tax)
admin.site.register(Deduction)
admin.site.register(Benefit)
