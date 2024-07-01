# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth    import AuthMiddlewareStack
from .urls            import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lernspiel_server.settings")

# application = ProtocolTypeRouter({
#     "http":      get_asgi_application(),
#     "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
# })

# TODO: Prototype - Remove again
from channels.layers            import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls                import path

class BroadcastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('broadcast', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('broadcast', self.channel_name)

    async def receive(self, text_data):
        print(">>>>>>> Received: %s" % text_data)
        await self.channel_layer.group_send('broadcast', {'type': 'broadcast_message', 'message': text_data})

    async def broadcast_message(self, event):
        print(">>>>>>> Sending: %s" % event['message'])
        await self.send(event['message'])

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('broadcast', BroadcastConsumer.as_asgi()),
        ])
    ),
})

channel_layer = get_channel_layer()
