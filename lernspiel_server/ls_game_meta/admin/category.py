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

class CategoryTInline(admin.TabularInline):
    model = models.Category_T
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    model           = models.Category
    search_fields   = ["name"],
    list_display    = ["name", "parent", "position", "created_by", "created_at", "modified_by", "modified_at"]
    list_filter     = ["name", "parent", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_by", "created_at", "modified_by", "modified_at"]
    inlines         = [CategoryTInline]
    
    fieldsets = (
        (None, {
            "fields": ["name", "parent", "position"]
        }),
        (_("Last Changed"), {
            "fields": ["created_by", "created_at", "modified_by", "modified_at"]
        })
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Set created by / modified by user
        """
        # TODO: Automatically fill created_by / modified_by -> move to utils/base class
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields["created_by"].
        # form.base_fields["modified_by"].
        return form