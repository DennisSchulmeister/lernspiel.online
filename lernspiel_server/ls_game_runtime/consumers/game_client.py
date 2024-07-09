# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import asyncio, json, time, uuid
from asgiref.sync               import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class GameClient(AsyncWebsocketConsumer):
    """
    Websocket consumer for game clients. Usually this will be the browser-side of the
    game player app, but other type of clients are possible, too.

    TODO: Prototype - Replace with real implementation
    """
    async def connect(self):
        """
        Accept connection from a game client. This joins the client to the Channel Group of this 
        running game, adds the player to the player list and sends an update to all clients.
        """
        self.clients_group_name = "Prototype.GameClient"
        await self.channel_layer.group_add(self.clients_group_name, self.channel_name)

        await self.channel_layer.send("game-runner", {
            "type": "hello",
        })

        await self.accept()


        # TODO: Update players list
        # TODO: Send broadcast
        # await self.send(json.dumps(players))

    async def disconnect(self, close_code):
        """
        Process disconnection from a game client. This removes the client from the Channel Group of
        this running game, removes to player from the player list and sends an update to all clients.
        """
        self.channel_layer.group_discard(self.clients_group_name, self.channel_name)
        
        # TODO: Update players list
        # TODO: Send broadcast
        # await self.send(json.dumps(players))

    async def receive(self, text_data):
        """
        Process message from game client. In this prototype version, the message is simply broadcast
        to all clients, as the logic (still) resides fully client-side. However, the current score
        of each player is tracked so that it can be sent to all clients when the player list is mutated.
        """
        pass
        # TODO
        
        # data = json.loads(text_data)
        # player = data['player']
        # score = data['score']

        # players[player] = {'player': player, 'score': score}

        # # Send the updated list of players to all connections
        # await self.channel_layer.group_send("broadcast", {"type": "broadcast_message", "message": json.dumps(players)})

    async def broadcast_message(self, event):
        """
        React on a broadcast event triggered by one of the consumer instances and send the data
        to the game client we are responsible here.
        """
        message = event["message"]
        await self.send(message)