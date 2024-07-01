# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib           import admin
from django.utils.translation import gettext_lazy as _
from lernspiel_server.admin   import MediaFileInline
from ..                       import models

class BackgroundAdmin(admin.ModelAdmin):
    model           = models.Background
    search_fields   = ["name"]
    list_display    = ["name", "created_modified_by"]
    list_filter     = ["name", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    fields          = ["name", "created_modified_by"]
    inlines         = [MediaFileInline]

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Set created by / modified by user
    #     """
    #     # TODO: Automatically fill created_by / modified_by -> move to utils/base class
    #     form = super(models.Background, self).get_form(request, obj, **kwargs)
    #     # form.base_fields["created_by"].
    #     # form.base_fields["modified_by"].
    #     return form
