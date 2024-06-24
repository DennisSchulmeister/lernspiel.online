# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class QuizzesConfig(AppConfig):
    """
    Games Core: Core data model for all games. Defines the low-level base blocks for
    game types, game variants, game content and game sessions. Needs at least one
    extension app that extends these basic data types via multi-table inheritance
    for concrete game rules.
    """
    name         = "lernspiel_server.games.games_core"
    verbose_name = _("Games: Core")
