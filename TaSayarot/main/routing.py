from django.urls import path
from .consumers import LikeConsumer, ForumConsumer


websocket_urlpatterns = [
    path('ws/likes/', LikeConsumer.as_asgi()),
    path('ws/forum/', ForumConsumer.as_asgi())
]
