# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.utils.translation import gettext_lazy as _

from lernspiel_server.db import AbstractModel

# TODO: Generic model for players and non-players on a map.
# Generic coordinates in 2D, 3D, xD space
# Generic attributes that can be interpreted by the game variants as needed (captured flags, inventory, ...)
