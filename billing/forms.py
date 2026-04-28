from django import forms
from .models import Invoice, Customer


# =========================
# 🧾 INVOICE FORM
# =========================
class InvoiceForm(forms.ModelForm):
    customer_input = forms.CharField(
        label="Customer",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter customer name'
        })
    )

    class Meta:
        model = Invoice
        fields = ['tax', 'discount']
        widgets = {
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tax amount'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Discount amount'
            }),
        }

    # 🔥 CLEAN INPUT (IMPORTANT)
    def clean_customer_input(self):
        name = self.cleaned_data.get('customer_input').strip()

        if not name:
            raise forms.ValidationError("Customer name cannot be empty")

        return name


# =========================
# 👤 CUSTOMER FORM
# =========================
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Address'
            }),
        }