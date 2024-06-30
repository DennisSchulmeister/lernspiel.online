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
    model = meta.Category_T
    extra = 0

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
        # TODO: Automatically fill created_by / modified_by -> move to utils/base class
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields["created_by"].
        # form.base_fields["modified_by"].
        return form


# TODO: Utility class to simplify these three into one
# class PropertyMetaAdmin -> model, translations, class Inline, class Change
class PropertyMetaInline(admin.TabularInline):
    model            = meta.PropertyMeta
    extra            = 0
    show_change_link = True

class PropertyMetaTInline(admin.TabularInline):
    model = meta.PropertyMeta_T
    extra = 0

class PropertyMetaAdmin(admin.ModelAdmin):
    model   = meta.PropertyMeta
    inlines = [PropertyMetaTInline]


class EventMetaInline(admin.TabularInline):
    model            = meta.EventMeta
    extra            = 0
    show_change_link = True

class EventMetaTInline(admin.TabularInline):
    model = meta.EventMeta_T
    extra = 0

class EventMetaAdmin(admin.ModelAdmin):
    model   = meta.EventMeta
    inlines = [EventMetaTInline]



class SlotMetaInline(admin.TabularInline):
    model            = meta.SlotMeta
    extra            = 0
    show_change_link = True

class SlotMetaTInline(admin.TabularInline):
    model = meta.SlotMeta_T
    extra = 0

class SlotMetaAdmin(admin.ModelAdmin):
    model   = meta.SlotMeta
    inlines = [SlotMetaTInline]


class GameComponentMetaTInline(admin.TabularInline):
    model = meta.GameComponentMeta_T
    extra = 0

class GameComponentMetaAdmin(admin.ModelAdmin):
    model           = meta.GameComponentMeta
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


admin_site.register(meta.Category, CategoryAdmin)
admin_site.register(meta.GameComponentMeta, GameComponentMetaAdmin)
admin_site.register(meta.PropertyMeta, PropertyMetaAdmin)
admin_site.register(meta.EventMeta, EventMetaAdmin)
admin_site.register(meta.SlotMeta, SlotMetaAdmin)