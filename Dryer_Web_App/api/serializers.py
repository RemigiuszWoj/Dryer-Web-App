from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            # "code",
            "host",
            "orderer_name",
            "orderer_surname",
            "dryer_model",
            "create_at",
            "day_to_build",
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("orderer_name", "orderer_surname", "dryer_model")
