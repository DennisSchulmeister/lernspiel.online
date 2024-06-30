# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.urls import path
from . import consumers

app_name = "ls_game_runtime"

urlpatterns = [
    path('game_client/', consumers.GameClientWebsocketConsumer.as_asgi()),
]