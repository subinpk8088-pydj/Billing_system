from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Invoice, InvoiceItem, Payment

admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Payment)