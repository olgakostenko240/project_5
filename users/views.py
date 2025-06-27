from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import IsModer, IsStaff
from users.serializers import UserSerializers, PaymentSerializers, UserIsAuthenticatedSerializers
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializers
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ("payment_date",)
    search_fields = ("payment_method",)
    filterset_fields = (
        "payment_date",
        "payment_course",
        "payment_lesson",
        "payment_method",
    )

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        stripe_product_id = create_stripe_product(payment)
        price_id = create_stripe_price(payment, stripe_product_id)
        session_id, payment_link = create_stripe_session(price_id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny, ~IsModer,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    #serializer_class = UserSerializers
    permission_classes = (IsAuthenticated, IsModer | IsStaff)

    def get_serializer_class(self):
        if self.permission_classes:
            return UserIsAuthenticatedSerializers

        return UserSerializers


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (IsAuthenticated, IsModer | IsStaff)


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (IsAuthenticated, IsModer | IsStaff)


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (IsAuthenticated, ~IsModer | IsStaff)
