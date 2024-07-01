# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib         import admin
from lernspiel_server.admin import MediaFileInline
from ..                     import models

class BackgroundAdmin(admin.ModelAdmin):
    model   = models.Background
    inlines = [MediaFileInline]
