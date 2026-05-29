from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/shops/', consumers.ShopStatusConsumer.as_asgi()),
]