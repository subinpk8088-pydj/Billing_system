from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import InvoiceItem


@receiver(post_delete, sender=InvoiceItem)
def restore_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity
    product.save()