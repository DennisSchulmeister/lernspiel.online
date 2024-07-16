# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib           import admin
from django.utils.translation import gettext_lazy as _
from ..                       import models

class GameIdAdmin(admin.ModelAdmin):
    model            = models.GameId
    list_display     = ["game_instance", "participant_role"]
    fields           = ["id", "game_instance", "participant_role"]
    readonly_fields  = ["id"]

class GameIdInline(admin.TabularInline):
    model            = models.GameId
    extra            = 1
    show_change_link = True
