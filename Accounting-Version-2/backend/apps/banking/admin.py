from django.contrib import admin
from .models import BankAccount, BankTransaction, BankReconciliation

admin.site.register(BankAccount)
admin.site.register(BankTransaction)
admin.site.register(BankReconciliation)
