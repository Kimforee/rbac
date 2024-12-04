from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsModerator(BasePermission):
    """
    Allows access only to moderator users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'moderator'

class IsAdminOrModerator(BasePermission):
    """
    Allows access to admin and moderator users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'moderator']
