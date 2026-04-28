from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# =========================
# 👤 CUSTOMER (PRODUCTION READY)
# =========================
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# 📦 PRODUCT (IMPROVED)
# =========================
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


# =========================
# 🧾 INVOICE (PROFESSIONAL VERSION)
# =========================
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def get_subtotal(self):
        return sum(item.get_total() for item in self.items.all())

    def get_total(self):
        return self.get_subtotal() + self.tax - self.discount

    def get_profit(self):
        return sum(item.get_profit() for item in self.items.all())

    def get_paid_amount(self):
        return sum(p.amount for p in self.payments.all())

    def get_balance(self):
        return self.get_total() - self.get_paid_amount()

    def is_paid(self):
        return self.get_balance() <= 0

    def __str__(self):
        return f"Invoice #{self.id}"


# =========================
# 📄 INVOICE ITEMS
# =========================
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def get_total(self):
        return self.price * self.quantity

    def get_profit(self):
        return (self.price - self.product.cost_price) * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# =========================
# 💳 PAYMENT (FIXED)
# =========================
class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} ({self.method})"