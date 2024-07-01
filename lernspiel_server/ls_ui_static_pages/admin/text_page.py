# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib         import admin
from lernspiel_server.admin import MediaFileInline
from .custom_css            import CustomCSSInline
from .menu_assignment       import MenuAssignmentInline
from ..                     import models

class TextPageTInline(admin.StackedInline):
    model = models.TextPage_T
    extra = 1

class TextPageAdmin(admin.ModelAdmin):
    model = models.TextPage
    inlines = [TextPageTInline, MediaFileInline, CustomCSSInline, MenuAssignmentInline]