# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GameTypeWheelOfFortunedConfig(AppConfig):
    """
    Wheel of fortune games: Players must guess a word or sentence by finding the right letters.
    """
    name         = "ls_games_fortune"
    verbose_name = _("Games: Wheel of Fortune")

    def ready(self):
        from ls_games_core.utils.game_types import register_game_type
        register_game_type("WHEEL_OF_FORTUNE", _("Wheel of Fortune"))
