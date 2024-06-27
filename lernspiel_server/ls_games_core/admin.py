# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django.utils.translation import gettext_lazy as _

from lernspiel_server.models import MediaFile
from .models import GameVariant, SourceFile

class MediaFileInline(GenericTabularInline):
    model        = MediaFile
    verbose_name = _("Media File")
    verbose_name_plural = _("Media Files")

class SourceFileInline(admin.TabularInline):
    model               = SourceFile
    verbose_name        = _("Source File")
    verbose_name_plural = _("Source Files")

class GameVariantAdmin(admin.ModelAdmin):
    model        = GameVariant
    list_display = ["name", "game_type", "par_content_type"]
    fields       = ["name", "game_type", "description"]
    inlines      = [MediaFileInline, SourceFileInline]

admin.site.register(GameVariant, GameVariantAdmin)
