from django.contrib import admin
from .models import (
    KYC, 
    Payment, 
    CustomUser, 
    Notification, 
    Transaction, 
    Support
)

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(Transaction)
admin.site.register(KYC)
admin.site.register(Support)

