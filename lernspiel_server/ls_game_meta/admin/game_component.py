# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib           import admin
from django.utils.translation import gettext_lazy as _
from lernspiel_server.admin   import MediaFileInline, SourceFileInline
from .property                import PropertyMetaInline
from .event                   import EventMetaInline
from .slot                    import SlotMetaInline
from ..                       import models

class GameComponentMetaTInline(admin.StackedInline):
    model = models.GameComponentMeta_T
    extra = 1

class GameComponentMetaAdmin(admin.ModelAdmin):
    model           = models.GameComponentMeta
    search_fields   = ["name", "category"]
    list_display    = ["name", "category", "created_by", "created_at", "modified_by", "modified_at"]
    list_filter     = ["name", "category", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_by", "created_at", "modified_by", "modified_at"]
    inlines         = [GameComponentMetaTInline, PropertyMetaInline, EventMetaInline, SlotMetaInline, MediaFileInline, SourceFileInline]

    fieldsets = (
        (None, {
            "fields": ["name", "category", "thumbnail"]
        }),
        (_("Last Changed"), {
            "fields": ["created_by", "created_at", "modified_by", "modified_at"]
        })
    )
