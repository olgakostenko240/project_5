from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserCreateApiView, PaymentViewSet, UserListApiView


app_name = UsersConfig.name

router = SimpleRouter()
router.register("payment", PaymentViewSet)

urlpatterns = [
    path("user/", UserListApiView.as_view(), name="user_list"),
    path("user/create/", UserCreateApiView.as_view(), name="user_create"),
]

urlpatterns += router.urls
