# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib                    import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation          import gettext_lazy as _
from lernspiel_server.admin            import MediaFileInline
from .custom_css                       import CustomCSSInline
from ..                                import models

class TextPageTInline(admin.StackedInline):
    model  = models.TextPage_T
    extra  = 1
    fields = ["language", "format", "title", "content"]

    def get_formset(self, request, obj=None, **kwargs):
        """
        Add CSS classes to the some fields to simplify access in JavaScript. This is done
        to dynamically create a rich-text content editor for the chosen format.
        """
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form

        form.base_fields["format"].widget.attrs["class"] = "__format"
        form.base_fields["content"].widget.attrs["class"]  = "__content"
        
        return formset
    
class MenuAssignmentInline(GenericTabularInline):
    model   = models.MenuAssignment
    extra   = 1
    classes = ["collapse"]

class TextPageAdmin(admin.ModelAdmin):
    change_form_template = "ls_ui_text_pages/admin/textpage/change_form.html"

    model = models.TextPage
    search_fields   = ["name", "url"]
    list_display    = ["name", "url", "page_type", "login_required", "is_published", "published", "publish_start", "publish_end"]
    list_filter     = ["page_type", "login_required", "published", "publish_start", "publish_end", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["is_published", "created_modified_by"]
    inlines         = [TextPageTInline, MediaFileInline, CustomCSSInline, MenuAssignmentInline]

    fieldsets = (
        (None, {
            "fields": ["name", "url", "page_type"],
        }),
        (_("Display Options"), {
            "fields": ["show_title", "background"],
            "classes": ["collapse"],
        }),
        (_("Publication"), {
            "fields": ["login_required", "published", "publish_start", "publish_end", "created_modified_by"]
        })
    )