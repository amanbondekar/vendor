from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {'name': 'Vendor1', 'contact_details': 'Contact1', 'address': 'Address1', 'vendor_code': 'V1'}
        self.vendor = Vendor.objects.create(**self.vendor_data)

        self.purchase_order_data = {
            'po_number': 'PO123',
            'vendor': self.vendor,
            'order_date': '2023-01-01',
            'delivery_date': '2023-02-01',
            'items': {'item1': 5, 'item2': 10},
            'quantity': 15,
            'status': 'pending',
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_retrieve_vendor(self):
        url = reverse('vendor-retrieve-update-delete', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)

    def test_create_purchase_order(self):
        url = reverse('purchase-order-list-create')
        response = self.client.post(url, self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-delete', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order.po_number)
