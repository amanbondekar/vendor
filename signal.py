from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .performance_matric import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, calculate_fulfillment_rate

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        # Update the vendor metrics when a completed purchase order is saved
        vendor = instance.vendor
        vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
        vendor.average_response_time = calculate_average_response_time(vendor)
        vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)
        vendor.save()
