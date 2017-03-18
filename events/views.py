from rest_framework import viewsets

from .models import Flight, Plan
from .serializers import FlightSerializer, PlanSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
