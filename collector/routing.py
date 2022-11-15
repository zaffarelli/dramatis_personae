from django.urls import re_path

from collector.consumers import CollectorConsumer

ws_urlpatterns = [
    re_path("^websocket/collector/$", CollectorConsumer.as_asgi()),
]
