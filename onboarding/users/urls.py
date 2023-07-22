"""Users URL config."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from onboarding.users.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshPairView,
    MyUserViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"users", MyUserViewSet, basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path(
        "api/users/login/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/users/login/refresh/",
        CustomTokenRefreshPairView.as_view(),
        name="token_refresh",
    ),
    path("api/", include(router.urls)),
]
