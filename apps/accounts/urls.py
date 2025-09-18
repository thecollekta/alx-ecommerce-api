# apps/accounts/urls.py

"""
URL configuration for the accounts app.
Defines API endpoints for user authentication and profile management.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import (
    CustomTokenRefreshView,
    UserLoginView,
    UserLogoutView,
    UserProfileViewSet,
    UserRegistrationView,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r"profiles", UserProfileViewSet, basename="user-profile")
router.register(
    r"users", UserProfileViewSet, basename="user"
)  # For admin user management

# Add app_name for namespace
app_name = "accounts"

# Define URL patterns
urlpatterns = [
    # Authentication endpoints
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    # JWT token management
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    # Include router URLs last
    path("", include(router.urls)),
]
