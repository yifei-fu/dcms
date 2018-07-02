from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrAdminOtherwiseReadOnly(BasePermission):

    def has_object_permission(self, request, view, instance):
        if request.method in permissions.SAFE_METHODS:  # read-only methods
            return True
        else:
            return request.user.is_staff or (request.user and instance.author.id == request.user.id)
