from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'receiver__username', 'amount')
    ordering = ('-timestamp',)
    
    
admin.site.register(Transaction, TransactionAdmin)
