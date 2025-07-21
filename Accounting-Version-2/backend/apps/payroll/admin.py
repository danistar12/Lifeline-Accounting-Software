from django.contrib import admin
from .models import Employee, Payroll, PayrollDeduction

admin.site.register(Employee)
admin.site.register(Payroll)
admin.site.register(PayrollDeduction)
