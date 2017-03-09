from rest_framework import viewsets

from .models import Membership
from .serializers import MembershipSerializer



class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
