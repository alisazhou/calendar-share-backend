from rest_framework import viewsets

from .models import Calendar
from .serializers import CalendarSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
