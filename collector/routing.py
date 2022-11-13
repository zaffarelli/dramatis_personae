from django.urls import path

from collector.consumers import CollectorConsumer

ws_urlpatterns = [
    path("websocket/collector/", CollectorConsumer.as_asgi()),
]
