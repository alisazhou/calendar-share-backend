"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from addresses.views import AddressViewSet
from calendars.views import CalendarViewSet
from events.views import FlightViewSet, PlanViewSet
from memberships.views import MembershipViewSet
from profiles.views import ProfileViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, 'address')
router.register(r'calendars', CalendarViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'profiles', ProfileViewSet, 'profile')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^obtain-auth-token/', views.obtain_auth_token),
]
