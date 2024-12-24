from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet

user_router = DefaultRouter()
user_router.register("user", UserModelViewSet, "user")

auth_paths = [
    path("auth/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("", include(user_router.urls)),
    *auth_paths,
]
