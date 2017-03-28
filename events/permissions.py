from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        return curr_user.is_staff or obj.owner == curr_user
