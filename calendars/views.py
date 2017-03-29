from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Calendar
from .permissions import IsMemberOrAdmin
from .serializers import CalendarSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsMemberOrAdmin)
    serializer_class = CalendarSerializer

    def get_queryset(self):
        curr_user = self.request.user
        if curr_user.is_staff:
            return Calendar.objects.all()
        else:
            return curr_user.calendars_shared.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
