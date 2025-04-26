from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny

from users.models import User, Payment
from users.serializers import UserSerializers, PaymentSerializers


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ('payment_date',)
    search_fields = ('payment_method',)
    filterset_fields = ('payment_date', 'payment_course', 'payment_lesson', 'payment_method',)


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
