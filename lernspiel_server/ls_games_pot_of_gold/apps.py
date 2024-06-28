# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GameTypePotOfGoldConfig(AppConfig):
    """
    Pot of gold games: These are very simple games where each player draws a random entry
    from a set. Players must then explain the entry.
    """
    name         = "ls_games_pot_of_gold"
    verbose_name = _("Games: Pot of Gold")

    def ready(self):
        from ls_games_core.models import register_game_type
        register_game_type("POT_OF_GOLD", _("Pot of Gold"))
