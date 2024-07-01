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

class CustomCSS(db_utils.UUIDMixin):
    """
    Custom CSS Stylesheet for text pages or page types.
    """
    # Link to related model
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Stylesheet data
    name     = models.CharField(verbose_name=_("Name"), max_length=255)
    position = models.PositiveSmallIntegerField(verbose_name=_("Position"))
    css_code = models.TextField(verbose_name=_("CSS Code"), blank=True, null=True)

    # Django meta information
    class Meta:
        verbose_name        = _("Custom Stylesheet")
        verbose_name_plural = _("Custom Stylesheets")
        ordering            = ["name", "position"]