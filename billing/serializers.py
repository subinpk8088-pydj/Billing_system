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