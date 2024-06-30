# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import traceback

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .custom_site import admin_site
from ..models import Site, User, UserGroup, Language


class SiteAdmin(admin.ModelAdmin):
    model              = Site
    list_display       = ["id", "domain", "name"]
    list_display_links = ["id", "domain"]
    search_fields      = ["domain", "name"]

    fieldsets = (
        (None, {
            "fields": ["id", "domain", "name"]
        }),
        (_("Theme Parameters (CSS)"), {
            "fields": ["logo", "logo_width", "header_bg", "link_color"]
        })
    )

admin_site.register(Site, SiteAdmin)


class LanguageAdmin(admin.ModelAdmin):
    model              = Language
    list_display       = ["language", "name"]
    list_display_links = ["language", "name"]
    search_fields      = ["language", "name"]
    fields             = ["language", "name"]

admin_site.register(Language, LanguageAdmin)


@admin.action(description=_("Reset API key of selected users"))
def reset_api_key(modeladmin, request, queryset):
    """
    Reset the API key of the selected users and send the new key via e-mail.
    """
    for user in queryset:
        try:
            user.reset_api_key(save_and_send_email=True)
        except ValidationError as ex:
            traceback.print_exc()
            modeladmin.message_user(request, str(" ".join(ex.messages)), messages.WARNING)

class CustomUserAdmin(UserAdmin):
    """
    Sub-class of Django's User Admin to integrate the additional fields of
    Application Users.
    """
    actions = (reset_api_key,)
    list_display = UserAdmin.list_display + ("user_type", "date_expires",)
    list_filter  = UserAdmin.list_filter + ("user_type", "date_expires",)

    def get_form(self, request, obj=None, **kwargs):
        """
        Override e-mail to be obligatory.
        See: https://stackoverflow.com/a/66562177
        """
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["email"].required = True
        return form

CustomUserAdmin.fieldsets[0][1]["fields"] += ("user_type",)
CustomUserAdmin.fieldsets[1][1]["fields"] += ("description", "picture",) 
CustomUserAdmin.fieldsets[3][1]["fields"] += ("date_expires",)

CustomUserAdmin.add_fieldsets[0][1]["fields"] = ("username", "user_type", "email",)

admin_site.register(User, CustomUserAdmin)
admin_site.register(UserGroup, GroupAdmin)