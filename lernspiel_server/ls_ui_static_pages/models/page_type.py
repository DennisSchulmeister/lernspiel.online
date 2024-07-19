# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from typing                             import Optional
from django.contrib.contenttypes.fields import GenericRelation
from django.db                          import models
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from .background                        import Background
from .custom_css                        import CustomCSS
from .menu_assignment                   import MenuAssignment

class PageType(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    Page type the defines the template, menus and custom CSS of one ore more pages.
    """
    STANDARD   = "ls_ui_text_pages/pagetype/standard.html"
    CENTERED   = "ls_ui_text_pages/pagetype/centered.html"
    FULLSCREEN = "ls_ui_text_pages/pagetype/fullscreen.html"

    _TEMPLATES = {
        STANDARD:   _("Standard Text Page"),
        CENTERED:   _("Centered Content"),
        FULLSCREEN: _("Fullscreen Content"),
    }

    name       = models.CharField(verbose_name=_("Name"), max_length=255)
    template   = models.CharField(verbose_name=_("Template"), max_length=255, choices=_TEMPLATES)
    background = models.ForeignKey(Background, verbose_name=_("Background"), on_delete=models.SET_NULL, null=True, blank=True)
    menus      = GenericRelation(MenuAssignment, help_text=_("Use this to override the menu assignments from the page type."))
    custom_css = GenericRelation(CustomCSS)
   
    class Meta:
        verbose_name        = _("Page  Type")
        verbose_name_plural = _("Page Types")
        ordering            = ["name",]

        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

class PageType_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(PageType, on_delete=models.CASCADE, related_name="translations")
    title  = models.CharField(verbose_name=_("Title"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass