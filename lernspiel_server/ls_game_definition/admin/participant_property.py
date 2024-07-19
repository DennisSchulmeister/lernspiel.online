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

class ParticipantPropertyTInline(admin.TabularInline):
    model = models.ParticipantProperty_T
    extra = 1

class ParticipantPropertyAdmin(admin.ModelAdmin):
    model        = models.ParticipantProperty
    inlines      = [ParticipantPropertyTInline]
    list_display = ["parent", "name", "data_type", "length", "is_array"]
    
    fieldsets = (
        (None, {
            "fields": ["parent", "name"],
        }),
        (_("Type Information"), {
            "fields": ["data_type", "length", "is_array"],
        })
    )

class ParticipantPropertyInline(admin.TabularInline):
    model            = models.ParticipantProperty
    extra            = 1
    show_change_link = True