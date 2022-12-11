import backend.tmp_main as backend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import CreateOrderSerializer, OrderSerializer


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CreateOrderView(APIView):
    serializer_class = CreateOrderSerializer

    def post(self, reqest, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=reqest.data)
        if serializer.is_valid():
            orderer_name = serializer.data.get("orderer_name")
            orderer_surname = serializer.data.get("orderer_surname")
            dryer_model = serializer.data.get("dryer_model")
            host = self.request.session.session_key
            queryset = Order.objects.filter(host=host)
            backend.manin()
            if queryset.exists():
                order = queryset[0]
                order.orderer_name = orderer_name
                order.orderer_surname = orderer_surname
                order.dryer_model = dryer_model
                order.save(
                    update_fields=["orderer_name", "orderer_surname", "dryer_model"]
                )

                return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
            else:
                order = Order(
                    host=host,
                    orderer_name=orderer_name,
                    orderer_surname=orderer_surname,
                    dryer_model=dryer_model,
                )
                order.save()
                return Response(
                    OrderSerializer(order).data, status=status.HTTP_201_CREATED
                )

        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )
