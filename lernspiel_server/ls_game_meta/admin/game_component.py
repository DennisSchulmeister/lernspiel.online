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
    list_display    = ["name", "category", "created_modified_by"]
    list_filter     = ["name", "category", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    fields          = ["name", "category", "thumbnail", "created_modified_by"]
    inlines         = [GameComponentMetaTInline, PropertyMetaInline, EventMetaInline, SlotMetaInline, MediaFileInline, SourceFileInline]

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Set created by / modified by user
    #     """
    #     # TODO: Automatically fill created_by / modified_by -> move to utils/base class
    #     form = super(models.GameComponentMeta, self).get_form(request, obj, **kwargs)
    #     # form.base_fields["created_by"].
    #     # form.base_fields["modified_by"].
    #     return form
