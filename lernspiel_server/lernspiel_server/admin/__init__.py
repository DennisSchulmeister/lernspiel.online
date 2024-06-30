# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.admin import GroupAdmin

from .custom_site  import *
from .file_uploads import *
from .language     import *
from .site         import *
from .user         import *

from ..models import User, UserGroup

admin_site = CustomAdminSite()

admin_site.register(Site, SiteAdmin)
admin_site.register(Language, LanguageAdmin)
admin_site.register(User, CustomUserAdmin)
admin_site.register(UserGroup, GroupAdmin)