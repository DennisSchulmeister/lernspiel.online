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
    # path("join/", RedirectView.as_view(url="/")),
    # path("edit/", RedirectView.as_view(url="/")),

    path("join/<key>", views.join_game, name="join-game"),
    path("edit/<key>", views.edit_game, name="edit-game"),
]