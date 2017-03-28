from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Membership
from .permissions import IsCalendarOwnerOrAdmin, IsMemberOrAdmin
from .serializers import MembershipSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return (IsAuthenticated(), IsCalendarOwnerOrAdmin())
        else:
            return (IsAuthenticated(), IsMemberOrAdmin())

    def get_queryset(self):
        curr_user = self.request.user
        if curr_user.is_staff:
            return Membership.objects.all()
        else:
            return curr_user.membership_set.all()
