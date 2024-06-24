# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LibrariesConfig(AppConfig):
    """
    Open world games: These are games like "capture the flag", where the players can freely
    move around on map and interact with their environment.
    """
    name         = "lernspiel_server.games.open_world"
    verbose_name = _("Games: Open World")
