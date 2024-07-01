# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.http               import HttpResponse
from django.shortcuts          import redirect
from django.urls               import reverse
from django.utils.translation  import gettext_lazy as _
from django.views.generic.base import TemplateView

# TODO: Prototype - Change

class JoinGame(TemplateView):
    template_name = "ls_ui_game_player/join.html"

    def post(self, request, *args, **kwargs):
        game_code   = request.POST.get("game_code")
        player_name = request.POST.get("play_namer")

        if not game_code or not player_name:
            return self.render_to_response({"error_message": _("Game code and player name are required.")})

        url = reverse("ls_ui_game_player:play-game", kwargs = {
            "game_code": game_code,
            "player_name": player_name,
        })
        
        return redirect(url)

class PlayGame(TemplateView):
    template_name = "ls_ui_game_player/play.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game_code"]   = self.kwargs["game_code"]
        context["player_name"] = self.kwargs["player_name"]
        return context