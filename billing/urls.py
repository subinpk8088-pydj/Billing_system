from django.urls import path
from .views import api_products, api_invoices, api_invoice_detail
from .views import (
    create_invoice, invoice_list, invoice_detail, invoice_pdf,
    product_list, add_product
)

urlpatterns = [
    path('create/', create_invoice),
    path('invoices/', invoice_list),
    path('invoice/<int:id>/', invoice_detail),
    path('invoice/<int:id>/pdf/', invoice_pdf),

    # ✅ NEW
    path('products/', product_list),
    path('products/add/', add_product),
    
    # API routes
path('api/products/', api_products),
path('api/invoices/', api_invoices),
path('api/invoice/<int:id>/', api_invoice_detail),
]