# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _

from lernspiel_server.models import MediaFile
from .models import GameVariant, SourceFile, GAME_TYPES

class MediaFileInline(GenericTabularInline):
    model               = MediaFile
    verbose_name        = _("Media File")
    verbose_name_plural = _("Media Files")

class SourceFileInline(admin.TabularInline):
    model               = SourceFile
    verbose_name        = _("Source File")
    verbose_name_plural = _("Source Files")

class GameVariantAdmin(admin.ModelAdmin):
    model        = GameVariant
    list_display = ["name", "game_type", "par_content_type"]
    inlines      = [MediaFileInline, SourceFileInline]

    def get_form(self, request, obj=None, **kwargs):
        """
        Restrict the allowed game types in the form. Must be done by modifying the
        form at runtime, because the choices depend on the installed apps. Due to
        the order in which Django initializes everything the list is only known,
        when all apps are fully initialized, including their models, forms, admins etc.
        """
        return forms.modelform_factory(GameVariant,
            fields  = ["name", "game_type", "description"],
            widgets = {"game_type": forms.Select(choices=GAME_TYPES)},
        )

admin.site.register(GameVariant, GameVariantAdmin)
