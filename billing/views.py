from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from .models import Product, Invoice, InvoiceItem
from .forms import InvoiceForm
from .utils import render_to_pdf


# ✅ CREATE INVOICE
@login_required
def create_invoice(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = InvoiceForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    invoice = form.save(commit=False)
                    invoice.created_by = request.user
                    invoice.save()

                    product_ids = request.POST.getlist('product')
                    quantities = request.POST.getlist('quantity')

                    for i in range(len(product_ids)):
                        if not quantities[i]:
                            continue

                        product = get_object_or_404(Product, id=product_ids[i])
                        qty = int(quantities[i])

                        if qty <= 0:
                            continue

                        InvoiceItem.objects.create(
                            invoice=invoice,
                            product=product,
                            quantity=qty,
                            price=product.price
                        )

                messages.success(request, "Invoice created successfully ✅")
                return redirect('/billing/invoices/')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    else:
        form = InvoiceForm()

    return render(request, 'billing/create_invoice.html', {
        'form': form,
        'products': products
    })


# ✅ LIST ALL INVOICES
@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')

    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices
    })


# ✅ INVOICE DETAIL
@login_required
def invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    items = invoice.items.all()

    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
        'items': items
    })


# ✅ PDF DOWNLOAD
@login_required
def invoice_pdf(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    items = invoice.items.all()

    context = {
        'invoice': invoice,
        'items': items
    }

    return render_to_pdf('billing/invoice_pdf.html', context)


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'billing/product_list.html', {
        'products': products
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if name and price and stock:
            Product.objects.create(
                name=name,
                price=price,
                stock=stock
            )
            messages.success(request, "Product added successfully")
            return redirect('/billing/products/')

        else:
            messages.error(request, "All fields required")

    return render(request, 'billing/add_product.html')


from rest_framework import serializers
from .models import Product, Invoice, InvoiceItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'created_at', 'tax', 'discount', 'items', 'total']

    def get_total(self, obj):
        return obj.get_total()

@api_view(['GET'])
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_invoices(request):
    invoices = Invoice.objects.all()
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data)