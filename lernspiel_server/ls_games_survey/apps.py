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
    Survey games: Allows to create simple polls and surveys.
    """
    name         = "ls_games_survey"
    verbose_name = _("Games: Surveys and Polls")