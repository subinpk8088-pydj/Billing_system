from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse

from .models import Product, Invoice, InvoiceItem, Payment, Customer
from .forms import InvoiceForm
from .utils import render_to_pdf
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth

from .models import Product, Invoice, InvoiceItem, Payment, Customer
from .forms import InvoiceForm
from .utils import render_to_pdf


# =========================
# 🔥 DASHBOARD
# =========================
@login_required
def dashboard(request):
    invoices = Invoice.objects.all()

    # FILTER
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if start_date and end_date:
        invoices = invoices.filter(created_at__date__range=[start_date, end_date])

    # BASIC STATS
    total_revenue = sum([inv.get_total() for inv in invoices])
    total_invoices = invoices.count()
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=5)
    recent_invoices = invoices.order_by('-created_at')[:5]

    # MONTHLY REVENUE
    monthly_data = (
        invoices
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum(F('items__price') * F('items__quantity')))
        .order_by('month')
    )

    months = []
    totals = []

    for data in monthly_data:
        months.append(data['month'].strftime('%b %Y'))
        totals.append(float(data['total'] or 0))

    # TOP PRODUCTS
    top_products = (
        InvoiceItem.objects
        .filter(invoice__in=invoices)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    top_product_names = [p['product__name'] for p in top_products]
    top_product_sales = [p['total_sold'] for p in top_products]

    # PAYMENT METHODS
    payment_data = (
        Payment.objects
        .filter(invoice__in=invoices)
        .values('method')
        .annotate(total=Sum('amount'))
    )

    payment_labels = [p['method'] for p in payment_data]
    payment_totals = [float(p['total']) for p in payment_data]

    return render(request, 'billing/dashboard.html', {
        'total_revenue': total_revenue,
        'total_invoices': total_invoices,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'recent_invoices': recent_invoices,
        'months': months,
        'totals': totals,
        'top_product_names': top_product_names,
        'top_product_sales': top_product_sales,
        'payment_labels': payment_labels,
        'payment_totals': payment_totals,
    })


# =========================
# 🧾 CREATE INVOICE
# =========================
from .models import Customer

@login_required
def create_invoice(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = InvoiceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['customer_input']

            # create or get customer
            customer, _ = Customer.objects.get_or_create(name=name)

            invoice = form.save(commit=False)
            invoice.customer = customer
            invoice.created_by = request.user
            invoice.save()

            product_ids = request.POST.getlist('product')
            quantities = request.POST.getlist('quantity')

            for i in range(len(product_ids)):
                product = Product.objects.get(id=product_ids[i])
                qty = int(quantities[i])

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=qty,
                    price=product.price
                )

            return redirect('invoice_list')

    else:
        form = InvoiceForm()

    return render(request, 'billing/create_invoice.html', {
        'form': form,
        'products': products
    })

# =========================
# 📄 LIST
# =========================
@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})


# =========================
# 🔍 DETAIL
# =========================
@login_required
def invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
        'items': invoice.items.all()
    })


# =========================
# 📄 PDF
# =========================
@login_required
def invoice_pdf(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    return render_to_pdf('billing/invoice_pdf.html', {
        'invoice': invoice,
        'items': invoice.items.all()
    })


# =========================
# 📊 DASHBOARD PDF
# =========================
@login_required
def dashboard_pdf(request):
    invoices = Invoice.objects.all()

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if start_date and end_date:
        invoices = invoices.filter(created_at__date__range=[start_date, end_date])

    return render_to_pdf('billing/dashboard_pdf.html', {
        'invoices': invoices,
        'total': sum([i.get_total() for i in invoices]),
        'start': start_date or "All Time",
        'end': end_date or ""
    })


# =========================
# PRODUCTS
# =========================
@login_required
def product_list(request):
    return render(request, 'billing/product_list.html', {
        'products': Product.objects.all()
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock')
        )
        messages.success(request, "Product added")
        return redirect('/billing/products/')

    return render(request, 'billing/add_product.html')
# =========================
# 🔌 CLEAN API
# =========================
def api_products(request):
    data = list(Product.objects.values('id', 'name', 'price', 'stock'))
    return JsonResponse(data, safe=False)


def api_invoices(request):
    data = list(Invoice.objects.values('id', 'customer_id', 'created_at'))
    return JsonResponse(data, safe=False)


def api_invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)

    items = list(invoice.items.values(
        'product__name', 'quantity', 'price'
    ))

    return JsonResponse({
        'id': invoice.id,
        'customer': invoice.customer.name,
        'items': items,
        'total': invoice.get_total()
    })
    
    
    
# =========================
# 👤 CUSTOMER MODULE
# =========================
from .forms import CustomerForm


@login_required
def customer_list(request):
    query = request.GET.get('q')

    customers = Customer.objects.all()

    if query:
        customers = customers.filter(name__icontains=query)

    return render(request, 'billing/customer_list.html', {
        'customers': customers,
        'query': query
    })


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Customer added")
            return redirect('/billing/customers/')

    else:
        form = CustomerForm()

    return render(request, 'billing/add_customer.html', {'form': form})


@login_required
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated")
            return redirect('/billing/customers/')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'billing/add_customer.html', {'form': form})


@login_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    messages.success(request, "Customer deleted")
    return redirect('/billing/customers/')    
    