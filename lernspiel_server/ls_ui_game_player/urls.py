# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.urls import path
from . import views

app_name = "ls_ui_game_player"

urlpatterns = [
    # TODO: Prototype - Change
    path("", views.JoinGame.as_view(), name="join-game"),
    path("game/<game_code>/<player_name>", views.PlayGame.as_view(), name="play-game"),
]