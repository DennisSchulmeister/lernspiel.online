# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from .category        import *
from .event           import *
from .event_parameter import *
from .game_component  import *
from .property        import *
from .slot            import *

from lernspiel_server.admin import admin_site
from .. import models

admin_site.register(models.Category, CategoryAdmin)
admin_site.register(models.GameComponentMeta, GameComponentMetaAdmin)
admin_site.register(models.PropertyMeta, PropertyMetaAdmin)
admin_site.register(models.EventMeta, EventMetaAdmin)
admin_site.register(models.EventParameterMeta, EventParameterMetaAdmin)
admin_site.register(models.SlotMeta, SlotMetaAdmin)