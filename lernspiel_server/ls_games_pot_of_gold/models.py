# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from lernspiel_server.db import AbstractModel
from ls_games_core.models import GameVariant

# TODO: 1:n pots per game, each pot with title/description/words
# Game settings:
#   - Players can choose a pot / Players get N random pots
#   - Pot order as configures / random
#   - How many words per pot must be drawn (setting for each pot)
