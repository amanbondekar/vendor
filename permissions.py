# permissions.py
from rest_framework import permissions

class IsVendorOfPurchaseOrder(permissions.BasePermission):
    """
    Custom permission to only allow the vendor associated with the purchase order to acknowledge it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the vendor associated with the purchase order
        return obj.vendor == request.user.vendor
