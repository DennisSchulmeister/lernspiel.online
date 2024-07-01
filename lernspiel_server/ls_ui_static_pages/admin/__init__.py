# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from lernspiel_server.admin import admin_site
from .background            import *
from .custom_css            import *
from .menu_entry            import *
from .menu                  import *
from .page_type             import *
from .snippet               import *
from .text_page             import *
from ..                     import models

admin_site.register(models.TextPage,   TextPageAdmin)
admin_site.register(models.PageType,   PageTypeAdmin)
admin_site.register(models.Menu,       MenuAdmin)
admin_site.register(models.MenuEntry,  MenuEntryAdmin)
admin_site.register(models.Snippet,    SnippetAdmin)
admin_site.register(models.Background, BackgroundAdmin)