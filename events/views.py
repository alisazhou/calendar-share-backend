from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Flight, Plan
from .permissions import IsOwnerOrAdmin
from .serializers import FlightSerializer, PlanSerializer


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)
    serializer_class = FlightSerializer

    def get_queryset(self):
        """
        If admin, return all flights. Else, return flights associated with
        calendars that the user is a member of.
        """
        curr_user = self.request.user
        if curr_user.is_staff:
            return Flight.objects.all()
        else:
            calendars_shared = list(curr_user.calendars_shared.all())
            flights_shared = Flight.objects.filter(calendar__in=calendars_shared)
            return flights_shared

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
