from rest_framework.permissions import BasePermission


class IsMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        is_member = curr_user in obj.members.all()
        return curr_user.is_staff or is_member
