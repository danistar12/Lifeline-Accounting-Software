from django.contrib import admin
from .models import Employee, Payroll, PayrollDeduction, TimeEntry

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('EmployeeID', 'CompanyID', 'Name', 'Email', 'HourlyRate', 'TaxWithholding', 'EmployeeNotes', 'CreatedDate')
	search_fields = ('Name', 'Email')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
	list_display = ('PayrollID', 'EmployeeID', 'PayPeriodStart', 'PayPeriodEnd', 'GrossPay', 'NetPay', 'TaxesWithheld', 'PaymentDate', 'CreatedDate')
	search_fields = ('PayrollID',)

@admin.register(PayrollDeduction)
class PayrollDeductionAdmin(admin.ModelAdmin):
	list_display = ('DeductionID', 'PayrollID', 'EmployeeID', 'DeductionType', 'Amount', 'CreatedDate')
	search_fields = ('DeductionType',)

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
	list_display = ('TimeEntryID', 'ProjectID', 'EmployeeID', 'WorkDate', 'Hours', 'TimeEntryNotes', 'Billable', 'Rate', 'CreatedDate')
	search_fields = ('TimeEntryNotes',)
