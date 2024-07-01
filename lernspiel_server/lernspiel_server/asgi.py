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
import json
from channels.layers            import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls                import path

players = {}

class BroadcastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Send the current list of players to the new connection
        await self.send(json.dumps(players))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        player = data['player']
        score = data['score']

        players[player] = {'player': player, 'score': score}

        # Send the updated list of players to all connections
        await self.channel_layer.group_send('broadcast', {'type': 'broadcast_message', 'message': json.dumps(players)})

    async def broadcast_message(self, event):
        message = event['message']
        await self.send(message)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('broadcast', BroadcastConsumer.as_asgi()),
        ])
    ),
})

channel_layer = get_channel_layer()
