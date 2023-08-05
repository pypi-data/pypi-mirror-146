import json
import os
import re
from urllib.parse import parse_qs

import aiohttp
import async_timeout
import requests
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer



FRONTEND_HOST = os.environ.get('FRONTEND_HOST', '')

class CacheConsumerException(Exception):
    pass

async def fetch(session, url, **kwargs):
    with async_timeout.timeout(100):
        async with session.get(url, **kwargs) as response:
            try:
                status = response.status
                data = await response.json(content_type=None)
                return (status, data)
            except Exception as e:
                print(e)
                return [-1, None]


def get_sub_init(path):
    return {
        'path': path,
        'subscribed': True,
        'dirty': False
    }

def is_detail(path):
    res = re.split('(.*\/)(.*)\/', path)
    try:
        int(res[2])
    except Exception:
        return False
    return True

class CacheConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        # self.group_name = None
        # self.channel_name = None
        self.subs = {}
        super().__init__(*args, **kwargs)

    async def subscribe(self, data):
        path = data['path']
        if path in self.subs:
            if self.subs[path]['subscribed']:
                return
            else:
                self.subs[path]['subscribed'] = True
                if self.subs[path]['dirty']:
                    self.subs[path]['dirty'] = False
                    await self.send_data_snapshot(path)
        else:
            self.subs[path] = get_sub_init(path)
            await self.send_data_snapshot(path)


    async def unsubscribe(self, data):
        path = data['path']
        if path in self.subs:
            self.subs[path]['subscribed'] = False

    @database_sync_to_async
    def is_shopper(self):
        return is_shopper(self.user)

    def get_query_params(self):
        return parse_qs(self.scope['query_string'].decode())

    async def send_data_snapshot(self, path):
        async with aiohttp.ClientSession() as session:
            [status, data] = await fetch(
                session,
                FRONTEND_HOST + "api/" + path,
                headers={
                    'Authorization': 'jwt ' + self.auth_token
                }
            )
            if status != 200:
                await self.send_message({
                    'path': path,
                    'action': 'insert',
                    'status': status,
                    'data': {
                        # **data,
                        "WS_CACHE_ERROR": True
                    }
                })
            else:
                await self.send_message({
                    'path': path,
                    'action': 'insert',
                    'status': status,
                    'data': data
                })

    async def send_message(self, data):
        # if "type" in data:
        #     data.pop("type")
        await self.send(text_data=json.dumps(data))

    async def set_dirty(self, event):
        path_stem = event["path"]
        path_stem_arg = None
        exact = False
        if "exact" in event:
            exact = event["exact"]
        if not exact:
            while path_stem != "/":
                try:
                    res = re.split('(.*\/)(.*)\/$', path_stem)
                    path_stem = res[1]
                    path_arg = res[2]
                except IndexError:
                    break

                try:
                    int(path_arg)
                    break
                except Exception:
                    continue


        if not exact and path_stem != "/":
            path_stem_arg = path_stem + path_arg + "/"
        else:
            if event["path"].endswith('/'):
                path_stem = event["path"][:-1]
            else:
                path_stem = event["path"]
        path_stem_reg = re.compile("^" + path_stem + "(\/?\?{0}|\/?\?{1}.*)$")
        for k in self.subs:
            is_match = False
            if (path_stem_arg and k.startswith(path_stem_arg)):
                is_match = True
            elif is_detail(k) and path_stem_reg.match(k):
                is_match = True
            elif k.startswith(path_stem):
                is_match = True

            if is_match:
                sub = self.subs[k]
                if sub["subscribed"]:
                    await self.send_data_snapshot(k)
                else:
                    sub["dirty"] = True


    async def connect(self):
        self.user = self.scope["user"]
        self.shopper_group_name = None
        self.group_name = None
        if self.user.is_anonymous:
            raise CacheConsumerException("No user authenticated")

        self.auth_token = self.get_query_params()["auth_token"][0]
        self.group_name = "ws_cache_{}".format(self.user.id)

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )


        if self.is_shopper():
            self.shopper_group_name = "ws_cache_shopper"
            await self.channel_layer.group_add(
                self.shopper_group_name,
                self.channel_name
            )

        await self.accept()


        await self.send_message({
            "action": "sys",
            "type": "connected",
            "text": "connection success"
        })

    async def disconnect(self, close_code):
        # leave group room
        try:
            if self.group_name:
                await self.channel_layer.group_discard(
                    self.group_name,
                    self.channel_name
                )
        except Exception:
            pass

        try:
            if self.shopper_group_name:
                await self.channel_layer.group_discard(
                    self.shopper_group_name,
                    self.channel_name
                )
        except Exception:
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)


    async def ping(self, data):
        await self.send_message({
            "action": "sys",
            "type": "pong",
        })

    commands = {
        'subscribe': subscribe,
        'unsubscribe': unsubscribe,
        'ping': ping
    }