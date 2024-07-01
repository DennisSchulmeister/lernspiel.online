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

class SnippetTInline(admin.StackedInline):
    model = models.Snippet_T
    extra = 1

class SnippetAdmin(admin.ModelAdmin):
    model           = models.Snippet
    search_fields   = ["name"]
    list_display    = ["name", "created_modified_by"]
    list_filter     = ["name", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    fields          = ["name", "created_modified_by"]
    inlines         = [SnippetTInline, MediaFileInline]
