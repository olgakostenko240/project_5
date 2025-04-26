from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateApiView, PaymentViewSet, UserListApiView


app_name = UsersConfig.name

router = SimpleRouter()
router.register("payment", PaymentViewSet)

urlpatterns = [
    path("user/", UserListApiView.as_view(), name="user_list"),
    path("user/create/", UserCreateApiView.as_view(), name="user_create"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]

urlpatterns += router.urls
