# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib import admin
from .menu_entry    import MenuEntryInline
from ..             import models

class MenuTInline(admin.TabularInline):
    model = models.Menu_T
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    model   = models.Menu
    inlines = [MenuTInline, MenuEntryInline]
