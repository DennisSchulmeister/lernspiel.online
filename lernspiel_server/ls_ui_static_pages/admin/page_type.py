# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib                    import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .custom_css                       import CustomCSSInline
from ..                                import models

class PageTypeTInline(admin.TabularInline):
    model = models.PageType_T
    extra = 1

class MenuAssignmentInline(GenericTabularInline):
    model = models.MenuAssignment
    extra = 1

class PageTypeAdmin(admin.ModelAdmin):
    model   = models.PageType
    search_fields   = ["name"]
    list_display    = ["name", "template", "background", "created_modified_by"]
    list_filter     = ["name", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    fields          = ["name", "template", "background", "created_modified_by"]
    inlines         = [PageTypeTInline, CustomCSSInline, MenuAssignmentInline]
