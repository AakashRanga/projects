from django.urls import path
from passwordless_auth.chat import consumers


websocket_urlpatterns = [
    path('users/', consumers.ChatConsumer.as_asgi()),
]