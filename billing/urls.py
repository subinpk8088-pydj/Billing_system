from django.urls import path
from .views import (
    dashboard, dashboard_pdf,

    create_invoice,
    invoice_list,
    invoice_detail,
    invoice_pdf,

    product_list,
    add_product,

    customer_list,
    add_customer,
    edit_customer,
    delete_customer,

    api_products,
    api_invoices,
    api_invoice_detail,
)

urlpatterns = [

    # =========================
    # 📊 DASHBOARD
    # =========================
    path('', dashboard, name='dashboard'),
    path('dashboard/pdf/', dashboard_pdf, name='dashboard_pdf'),


    # =========================
    # 🧾 INVOICES
    # =========================
    path('create/', create_invoice, name='create_invoice'),
    path('invoices/', invoice_list, name='invoice_list'),
    path('invoice/<int:id>/', invoice_detail, name='invoice_detail'),
    path('invoice/<int:id>/pdf/', invoice_pdf, name='invoice_pdf'),


    # =========================
    # 📦 PRODUCTS
    # =========================
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),


    # =========================
    # 👤 CUSTOMERS
    # =========================
    path('customers/', customer_list, name='customer_list'),
    path('customers/add/', add_customer, name='add_customer'),
    path('customers/edit/<int:id>/', edit_customer, name='edit_customer'),
    path('customers/delete/<int:id>/', delete_customer, name='delete_customer'),


    # =========================
    # 🔌 API
    # =========================
    path('api/products/', api_products, name='api_products'),
    path('api/invoices/', api_invoices, name='api_invoices'),
    path('api/invoice/<int:id>/', api_invoice_detail, name='api_invoice_detail'),
]