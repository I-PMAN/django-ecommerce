from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods (GET, HEAD, OPTIONS) for all,
    but only admins can POST, PUT, DELETE.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin
