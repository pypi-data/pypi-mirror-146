from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# def (user_id, path):
from django.utils.deprecation import MiddlewareMixin

from pgs_backend.mux_demux_consumer.utils import group_send_mux_demux


def send_alert(user_id, body, alert_type="info", **kwargs):
    async_to_sync(group_send_mux_demux)(
        "alerts_{}".format(user_id),
        {
            "type": "send_message",
            "alert_type": alert_type,
            "body": body,
            **kwargs
        }
    )

async def send_alert_async(user_id, body, alert_type="info", channel_layer=None, **kwargs):
    await group_send_mux_demux(
        "alerts_{}".format(user_id),
        {
            "type": "send_message",
            "alert_type": alert_type,
            "body": body,
            **kwargs
        }
    )

def send_set_path_dirty(user_id, path, **kwargs):
    channel_layer = get_channel_layer()
    if path.startswith("/api/"):
        path = path[5:]
    async_to_sync(channel_layer.group_send)(
        "ws_cache_{}".format(user_id),
        {
            "type": "set_dirty",
            "path": path,
            **kwargs
        }
    )

async def send_set_path_dirty_async(user_id, path, channel_layer=None, **kwargs):
    channel_layer = channel_layer or get_channel_layer()
    if path.startswith("/api/"):
        path = path[5:]
    await channel_layer.group_send(
        "ws_cache_{}".format(user_id),
        {
            "type": "set_dirty",
            "path": path,
            **kwargs
        }
    )

def send_set_shopper_path_dirty(path, **kwargs):
    channel_layer = get_channel_layer()
    if path.startswith("/api/"):
        path = path[5:]
    async_to_sync(channel_layer.group_send)(
        "ws_cache_shopper",
        {
            "type": "set_dirty",
            "path": path,
            **kwargs
        }
    )

async def send_set_shopper_path_dirty_async(path, channel_layer=None, **kwargs):
    channel_layer = channel_layer or get_channel_layer()
    if path.startswith("/api/"):
        path = path[5:]
    channel_layer.group_send(
        "ws_cache_shopper",
        {
            "type": "set_dirty",
            "path": path,
            **kwargs
        }
    )


class WsMiddlewareCache(MiddlewareMixin):

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.


        response = self.get_response(request)

        if request.method != "GET" and not request.user.is_anonymous:
            send_set_path_dirty(request.user.id, request.path)

        return response