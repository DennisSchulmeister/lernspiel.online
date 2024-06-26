# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("",                   RedirectView.as_view(url="/pages/start")),
    path("join/",              RedirectView.as_view(url="/")),
    path("edit/",              RedirectView.as_view(url="/")),

    path("join/<key>",         views.join_game, name="join-game"),
    path("edit/<key>",         views.edit_game, name="edit-game"),

    path("games/core/",        include("ls_games_core.urls")),
    path("games/open-world/",  include("ls_games_open_world.urls")),
    path("games/pot-of-gold/", include("ls_games_pot_of_gold.urls")),
    path("games/quiz/",        include("ls_games_quiz.urls")),
    path("libraries/",         include("ls_libraries.urls")),
    path("pages/",             include("ls_pages.urls")),
    path("admin/",             admin.site.urls),
]
