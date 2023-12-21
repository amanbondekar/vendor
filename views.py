# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from .performance_matric import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate,
)
from .permissions import IsVendorOfPurchaseOrder


class VendorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for creating and listing vendors.

    - POST: Create a new vendor.
    - GET: List all vendors.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific vendor.

    - GET: Retrieve a specific vendor's details.
    - PUT: Update a vendor's details.
    - DELETE: Delete a vendor.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for creating and listing purchase orders.

    - POST: Create a purchase order.
    - GET: List all purchase orders with an option to filter by vendor.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific purchase order.

    - GET: Retrieve details of a specific purchase order.
    - PUT: Update a purchase order.
    - DELETE: Delete a purchase order.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceEndpoint(generics.RetrieveAPIView):
    """
    API endpoint for retrieving performance metrics of a specific vendor.

    - GET: Retrieve a vendor's performance metrics, including
      on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate.
    """
    queryset = Vendor.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        vendor = self.get_object()
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data)

class UpdateAcknowledgmentEndpoint(generics.UpdateAPIView):
    """
    API endpoint for vendors to acknowledge purchase orders.

    - POST: Acknowledge a purchase order and trigger recalculation of average_response_time.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsVendorOfPurchaseOrder]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()

        # Recalculate average_response_time and update vendor metrics
        vendor = instance.vendor
        vendor.average_response_time = calculate_average_response_time(vendor)
        vendor.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
