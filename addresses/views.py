from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Address
from .permissions import IsOwnUserOrAdmin
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnUserOrAdmin)
    serializer_class = AddressSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        else:
            return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        curr_user = self.request.user
        prev_address = Address.objects.filter(user_id=curr_user.id)
        if prev_address:
            prev_address[0].delete()
        serializer.save(user=self.request.user)
