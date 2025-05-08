from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializers(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class UserIsAuthenticatedSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email",)