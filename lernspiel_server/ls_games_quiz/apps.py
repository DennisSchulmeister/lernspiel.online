# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GameTypeQuizConfig(AppConfig):
    """
    Quiz games: Knowledge games based on questions and answers.
    """
    name         = "ls_games_quiz"
    verbose_name = _("Games: Quiz")

    def ready(self):
        from ls_games_core.utils.game_types import register_game_type
        register_game_type("QUIZ", _("Quiz"))
