from django.urls import re_path

from pgs_backend.ws_cache.consumers import CacheConsumer

websocket_urlpatterns = [
    re_path(r'ws/get/$', CacheConsumer),

]