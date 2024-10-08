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

class CategoryTInline(admin.TabularInline):
    model = models.Category_T
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    model           = models.Category
    search_fields   = ["name"],
    list_display    = ["name", "parent", "position", "created_modified_by"]
    list_filter     = ["name", "parent", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    fields          = ["name", "parent", "position", "created_modified_by"]
    inlines         = [CategoryTInline]
