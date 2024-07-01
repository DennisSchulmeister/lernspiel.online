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

class EventMetaTInline(admin.TabularInline):
    model = models.EventMeta_T
    extra = 1

class EventMetaAdmin(admin.ModelAdmin):
    model   = models.EventMeta
    inlines = [EventMetaTInline]

class EventMetaInline(admin.TabularInline):
    model            = models.EventMeta
    extra            = 0
    show_change_link = True