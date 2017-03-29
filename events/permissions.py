from rest_framework.permissions import BasePermission

from calendars.models import Calendar


class IsMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        is_member = Calendar.objects.filter(id=obj.calendar.id).exists()
        return curr_user.is_staff or is_member
