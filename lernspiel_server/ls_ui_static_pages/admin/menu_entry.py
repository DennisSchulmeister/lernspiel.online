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

class MenuEntryTInline(admin.TabularInline):
    model = models.MenuEntry_T
    extra = 1

class MenuEntryAdmin(admin.ModelAdmin):
    model           = models.MenuEntry
    search_fields   = ["name"]
    list_display    = ["menu", "position", "name", "link_type", "new_window", "created_modified_by"]
    list_filter     = ["menu", "name", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    inlines         = [MenuEntryTInline]

    fieldsets = (
        (None, {
            "fields":["menu", "position", "name", "link_type", "new_window", "created_modified_by"],
        }),
        (_("Parameters"), {
            "fields": [
                "link_url",
                "link_page",
                "link_view_name", "link_view_par1", "link_view_par2", "link_view_par3", "link_view_par4", "link_view_par5"
            ],
        }),
    )

    # TODO: Hide link parameters not relevant to the current link type (in JavaScript)

class MenuEntryInline(admin.StackedInline):
    model            = models.MenuEntry
    extra            = 0
    show_change_link = True

    fieldsets = (
        (None, {
            "fields":["menu", "position", "name", "link_type", "new_window"],
        }),
        (_("Parameters"), {
            "fields": [
                "link_url",
                "link_page",
                "link_view_name", "link_view_par1", "link_view_par2", "link_view_par3", "link_view_par4", "link_view_par5"
            ],
        }),
    )

    # TODO: Hide link parameters not relevant to the current link type (in JavaScript)