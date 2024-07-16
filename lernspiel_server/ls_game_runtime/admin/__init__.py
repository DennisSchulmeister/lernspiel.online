# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from .game_instance         import *
from .game_id               import *
from lernspiel_server.admin import admin_site
from ..                     import models

admin_site.register(models.GameInstance, GameInstanceAdmin)
admin_site.register(models.GameId, GameIdAdmin)