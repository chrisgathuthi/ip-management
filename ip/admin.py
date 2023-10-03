from django.contrib import admin
from .models import IpAddress, CustomerInfo
# Register your models here.

admin.site.register(IpAddress)
admin.site.register(CustomerInfo)