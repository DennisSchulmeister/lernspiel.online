# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GamesConfig(AppConfig):
    """
    Game Development: This app provides the available game types and generally speaking
    contains anything that is needed to develop new game types, including management of
    developer keys and access via the Game SDK CLI.
    """
    name         = "lernspiel_server.gamedev"
    verbose_name = _("Game Development")
