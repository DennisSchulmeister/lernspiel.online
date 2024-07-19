# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from typing                             import Optional
from django.db                          import models
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from .menu                              import Menu
from .text_page                         import TextPage

class MenuEntry(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    An entry inside a menu, defining the link target.
    """
    NONE = "none"
    URL  = "url"
    PAGE = "page"
    VIEW = "view"

    _LINK_TYPES = {
        NONE: _("None / Section Title"),
        URL:  _("Static URL address"),
        PAGE: _("Text Page"),
        VIEW: _("Built-In View"),
    }

    LOGIN_ANY  = "any"
    LOGGED_IN  = "logged-in"
    LOGGED_OUT = "logged-out"

    _LOGIN_STATUS = {
        LOGIN_ANY:  _("Show always"),
        LOGGED_IN:  _("Show only for logged in users"),
        LOGGED_OUT: _("Show only for logged out users"),
    }

    # General information
    menu       = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name=_("Menu"), related_name="menu_entries")
    position   = models.PositiveSmallIntegerField(verbose_name=_("Position"))
    name       = models.CharField(verbose_name=_("Name"), max_length=255)
   
    # Link parameters
    link_type  = models.CharField(_("Link type"), max_length=10, choices=_LINK_TYPES, default=NONE, blank=False)
    link_url       = models.URLField(verbose_name=_("URL"), blank=True)
    link_page      = models.ForeignKey(TextPage, on_delete=models.SET_NULL, blank=True, null=True)
    link_view_name = models.CharField(_("View Name"), max_length=30, blank=True)
    link_view_par1 = models.CharField(_("Parameters"), max_length=30, blank=True)
    link_view_par2 = models.CharField("", max_length=30, blank=True)
    link_view_par3 = models.CharField("", max_length=30, blank=True)
    link_view_par4 = models.CharField("", max_length=30, blank=True)
    link_view_par5 = models.CharField("", max_length=30, blank=True)

    new_window     = models.BooleanField(verbose_name=_("Open in new window or tab"))
    login_status   = models.CharField(_("Login Status"), max_length=10, choices=_LOGIN_STATUS, default=LOGIN_ANY, blank=False)

    # Django meta information
    class Meta:
        verbose_name        = _("Menu Entry")
        verbose_name_plural = _("Menu Entries")
        ordering            = ["menu", "position"]
        indexes             = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name

    # Translated texts
    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

class MenuEntry_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(MenuEntry, on_delete=models.CASCADE, related_name="translations")
    title  = models.CharField(verbose_name=_("Title"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass