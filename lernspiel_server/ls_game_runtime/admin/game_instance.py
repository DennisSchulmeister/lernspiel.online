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

class GameInstanceAdmin(admin.ModelAdmin):
    model           = models.GameInstance
    search_fields   = ["definition_name", "channel"]
    list_display    = ["id", "definition", "running", "channel", "heartbeat", "created_modified_by"]
    list_filter     = ["created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["id", "created_modified_by"]

    fieldsets = (
        (None, {
            "fields": ["id", "definition_name", "created_modified_by"],
        }),
        (_("Game Runner"), {
            "fields": ["running", "channel", "heartbeat"],
        })
    )

    def get_queryset(self, request):
        return super(GameInstanceAdmin, self).get_queryset(request).select_related("definition")