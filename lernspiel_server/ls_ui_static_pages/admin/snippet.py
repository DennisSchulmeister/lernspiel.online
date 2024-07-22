# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib         import admin
from lernspiel_server.admin import MediaFileInline
from ..                     import models

class SnippetTInline(admin.StackedInline):
    model  = models.Snippet_T
    extra  = 1
    fields = ["language", "format", "content"]

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

class SnippetAdmin(admin.ModelAdmin):
    change_form_template = "ls_ui_text_pages/admin/textpage/change_form.html"
    
    model           = models.Snippet
    search_fields   = ["name"]
    list_display    = ["name", "created_modified_by"]
    list_filter     = ["name", "created_by", "created_at", "modified_by", "modified_at"]
    readonly_fields = ["created_modified_by"]
    fields          = ["name", "created_modified_by"]
    inlines         = [SnippetTInline, MediaFileInline]
