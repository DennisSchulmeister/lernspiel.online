# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from lernspiel_server.admin import admin_site
from .shared import MediaFileInline, SourceFileInline
from ..models import meta

class CategoryTInline(admin.TabularInline):
    model  = meta.Category_T

class CategoryAdmin(admin.ModelAdmin):
    model           = meta.Category
    search_fields   = ["name"],
    list_display    = ["name", "parent", "sort_order", "created_by", "created_at", "modified_by", "modified_at"]
    list_filter     = ["name", "parent", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_by", "created_at", "modified_by", "modified_at"]
    inlines         = [CategoryTInline]
    
    fieldsets = (
        (None, {
            "fields": ["name", "parent", "sort_order"]
        }),
        (_("Last Changed"), {
            "fields": ["created_by", "created_at", "modified_by", "modified_at"]
        })
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Set created by / modified by user
        """
        # TODO: Automatically fill created_by / modified_by
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields["created_by"].
        # form.base_fields["modified_by"].
        return form

admin_site.register(meta.Category, CategoryAdmin)


# TODO: Fix nested inlines -> https://stackoverflow.com/questions/14308050/django-admin-nested-inline
class GameComponentTInline(admin.TabularInline):
    model = meta.GameComponentMeta_T

class SlotTInline(admin.TabularInline):
    model = meta.SlotMeta_T

class PropertyTInline(admin.TabularInline):
    model = meta.PropertyMeta_T

class EventTInline(admin.TabularInline):
    model   = meta.EventMeta_T

class SlotInline(admin.StackedInline):
    model   = meta.SlotMeta
    inlines = [SlotTInline]

class PropertyInline(admin.StackedInline):
    model   = meta.PropertyMeta
    inlines = [PropertyTInline]

class EventInline(admin.StackedInline):
    model   = meta.EventMeta
    inlines = [EventTInline]

class GameComponentMetaAdmin(admin.ModelAdmin):
    model           = meta.GameComponentMeta
    search_fields   = ["name", "category"]
    list_display    = ["name", "category", "created_by", "created_at", "modified_by", "modified_at"]
    list_filter     = ["name", "category", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_by", "created_at", "modified_by", "modified_at"]
    inlines         = [GameComponentTInline, SlotInline, PropertyInline, EventInline, MediaFileInline, SourceFileInline]

    fieldsets = (
        (None, {
            "fields": ["name", "category", "thumbnail"]
        }),
        (_("Last Changed"), {
            "fields": ["created_by", "created_at", "modified_by", "modified_at"]
        })
    )

admin_site.register(meta.GameComponentMeta, GameComponentMetaAdmin)
