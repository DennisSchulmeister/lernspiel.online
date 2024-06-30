# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .. import models

class SlotMetaInline(admin.TabularInline):
    model            = models.SlotMeta
    extra            = 0
    show_change_link = True

class SlotMetaTInline(admin.TabularInline):
    model = models.SlotMeta_T
    extra = 0

class SlotMetaAdmin(admin.ModelAdmin):
    model   = models.SlotMeta
    inlines = [SlotMetaTInline]