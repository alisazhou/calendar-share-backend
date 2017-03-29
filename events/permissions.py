from rest_framework.permissions import BasePermission


class IsMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        is_member = obj.calendar in list(curr_user.calendars_shared.all())
        return curr_user.is_staff or is_member
