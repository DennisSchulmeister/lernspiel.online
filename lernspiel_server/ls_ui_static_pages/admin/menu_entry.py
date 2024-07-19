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

class MenuEntryTInline(admin.TabularInline):
    model = models.MenuEntry_T
    extra = 1

class MenuEntryAdmin(admin.ModelAdmin):
    change_form_template = "ls_ui_text_pages/admin/menu_entry/change_form.html"

    model           = models.MenuEntry
    search_fields   = ["name"]
    list_display    = ["menu", "position", "name", "login_status", "link_type", "new_window", "created_modified_by"]
    list_filter     = ["menu", "name", "login_status", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    inlines         = [MenuEntryTInline]

    fieldsets = (
        (None, {
            "fields":["menu", "position", "name", "login_status", "created_modified_by"],
        }),
        (_("Link"), {
            "fields": [
                "link_type",
                "link_url",
                "link_page",
                "link_view_name", "link_view_par1", "link_view_par2", "link_view_par3", "link_view_par4", "link_view_par5",
                "new_window",
            ],
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Add CSS classes to the link fields to simplify access in JavaScript. This is done
        to dynamically hide the fields that are not relevant for the selected link type.
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["link_view_name"].widget.attrs["class"] = "link_view"
        form.base_fields["link_view_par1"].widget.attrs["class"] = "link_view"
        form.base_fields["link_view_par2"].widget.attrs["class"] = "link_view"
        form.base_fields["link_view_par3"].widget.attrs["class"] = "link_view"
        form.base_fields["link_view_par4"].widget.attrs["class"] = "link_view"
        form.base_fields["link_view_par5"].widget.attrs["class"] = "link_view"
        return form

class MenuEntryInline(admin.StackedInline):
    model            = models.MenuEntry
    extra            = 0
    show_change_link = True

    fieldsets = (
        (None, {
            "fields":["menu", "position", "name", "link_type", "new_window"],
        }),
        (_("Parameters"), {
            "fields": [
                "link_url",
                "link_page",
                "link_view_name", "link_view_par1", "link_view_par2", "link_view_par3", "link_view_par4", "link_view_par5"
            ],
        }),
    )

    # TODO: Hide link parameters not relevant to the current link type (in JavaScript)