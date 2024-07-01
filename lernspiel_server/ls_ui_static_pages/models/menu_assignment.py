# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db                          import models
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from .menu                              import Menu

class MenuAssignment(db_utils.UUIDMixin):
    """
    Assignment of menus to the menu areas of a page or page type.
    """
    # Link to related model
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Menu assignment
    HEADER = "header"
    SIDE   = "side"
    FOOTER = "footer"

    _MENU_AREAS = {
        HEADER: _("Header"),
        SIDE:   _("Side"),
        FOOTER: _("Footer"),
    }

    area     = models.CharField(verbose_name=_("Area"), max_length=10, choices=_MENU_AREAS)
    position = models.PositiveSmallIntegerField(verbose_name=_("Position"))
    menu     = models.ForeignKey(Menu, verbose_name=_("Menu"), on_delete=models.CASCADE)

    # Django meta information
    class Meta:
        verbose_name        = _("Menu Assignment")
        verbose_name_plural = _("Menu Assignments")
        ordering            = ["area", "menu"]