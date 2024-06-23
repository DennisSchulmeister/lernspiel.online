# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GameroundsConfig(AppConfig):
    """
    Game Builder: This app allows users to build concrete games by customizing the available
    game types and adding their content.
    """
    name         = "lernspiel_server.gamebuilder"
    verbose_name = _("Game Builder")
