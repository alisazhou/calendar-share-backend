from rest_framework.permissions import BasePermission


class IsMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        return curr_user.is_staff or curr_user == obj.member


class IsCalendarOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        is_owner = curr_user == obj.calendar.owner
        return curr_user.is_staff or is_owner
