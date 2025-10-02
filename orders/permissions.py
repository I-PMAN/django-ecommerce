from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    """
    Customers can view their own orders.
    Admins can view & manage all orders.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_admin:
            return True
        # Customers can only access their own orders
        return obj.user == request.user
