from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Profile
from .permissions import IsOwnUserOrAdmin
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # allow anon users to create profiles
            return (AllowAny(),)
        else:
            return (IsAuthenticated(), IsOwnUserOrAdmin())

    def get_queryset(self):
        curr_user = self.request.user
        if curr_user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user_id=curr_user.id)
