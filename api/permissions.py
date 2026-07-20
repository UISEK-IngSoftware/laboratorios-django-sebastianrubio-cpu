# catalog/permissions.py
from rest_framework import permissions

class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Comprobar primero si el usuario está autenticado en el sistema
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)