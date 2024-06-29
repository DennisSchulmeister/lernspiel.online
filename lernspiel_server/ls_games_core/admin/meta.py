# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from lernspiel_server.admin import admin_site
from .shared import MediaFileInline, SourceFileInline
from ..models.meta import GameComponentMeta

# TODO
class GameComponentMetaAdmin(admin.ModelAdmin):
    model        = GameComponentMeta
    list_display = ["name",]
    inlines      = [MediaFileInline, SourceFileInline]

admin_site.register(GameComponentMeta, GameComponentMetaAdmin)
