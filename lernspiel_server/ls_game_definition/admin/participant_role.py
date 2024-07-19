# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib           import admin
from django.utils.translation import gettext_lazy as _
from .participant_property    import ParticipantPropertyInline
from ..                       import models

class ParticipantRoleTInline(admin.TabularInline):
    model = models.ParticipantRole_T
    extra = 1

class ParticipantRoleAdmin(admin.ModelAdmin):
    model        = models.ParticipantRole
    inlines      = [ParticipantRoleTInline, ParticipantPropertyInline]
    list_display = ["parent", "name", "limit"]

class ParticipantRoleInline(admin.TabularInline):
    model            = models.ParticipantRole
    extra            = 1
    show_change_link = True
