from django.urls import path

from .views import CreateOrderView, OrderView

urlpatterns = [
    path("order", OrderView.as_view()),
    path("create_order", CreateOrderView.as_view()),
]
