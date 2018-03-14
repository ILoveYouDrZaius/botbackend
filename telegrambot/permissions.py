from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

class OnlyOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
    
class Deny(permissions.BasePermission):
    """
    Always return False
    """
    def has_permission(self, request, view):
        return False
    # def has_object_permission(self, request, view, obj):
    #     return False