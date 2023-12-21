# metrics_calculator.py
from django.db.models import Count, Avg, F, Sum
from .models import Vendor, PurchaseOrder, HistoricalPerformance

def calculate_on_time_delivery_rate(vendor):
    completed_purchases = PurchaseOrder.objects.filter(vendor=vendor, status='completed').annotate(
        on_time_delivery=Count('pk', filter=F('delivery_date__lte', F('acknowledgment_date')))
    )
    total_completed_purchases = completed_purchases.count()

    if total_completed_purchases == 0:
        return 0.0

    on_time_deliveries = completed_purchases.aggregate(Sum('on_time_delivery'))['on_time_delivery__sum']
    return (on_time_deliveries / total_completed_purchases) * 100

def calculate_quality_rating_avg(vendor):
    completed_purchases = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating__isnull=True)
    
    if not completed_purchases.exists():
        return 0.0

    quality_rating_avg = completed_purchases.aggregate(Avg('quality_rating'))['quality_rating__avg']
    return quality_rating_avg

def calculate_average_response_time(vendor):
    acknowledged_purchases = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)

    if not acknowledged_purchases.exists():
        return 0.0

    response_times = acknowledged_purchases.annotate(
        response_time=F('acknowledgment_date') - F('issue_date')
    ).aggregate(Avg('response_time'))['response_time__avg']

    return response_times.total_seconds()

def calculate_fulfillment_rate(vendor):
    successful_purchases = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=True)

    total_purchases = vendor.purchaseorder_set.count()

    if total_purchases == 0:
        return 0.0

    fulfillment_rate = (successful_purchases.count() / total_purchases) * 100
    return fulfillment_rate
