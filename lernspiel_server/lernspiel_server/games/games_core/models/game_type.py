# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from ....core_platform.db import AbstractModel, CreatedModifiedByMixin
from ....core_platform.models import MediaFile

class GameType(AbstractModel, CreatedModifiedByMixin):
    """
    xxx
    """
    # content type for inheritance
    
    name        = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Game Type")
        verbose_name_plural = _("Game Types")
    
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

class GameVariant(AbstractModel, CreatedModifiedByMixin):
    """
    xxx
    """
    # content type for inheritance

    name        = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    media       = GenericRelation(MediaFile)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Game Variant")
        verbose_name_plural = _("Game Variants")
    
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

class ClientSourceFile(AbstractModel, CreatedModifiedByMixin):
    """
    Client-side source files with HTML, CSS, JS code to implement a brand-new
    game variant. Note, this way only the exiting game types
    """
    HTML = 1
    CSS  = 2
    JS   = 3

    _FILE_TYPES = (
        (HTML, _("HTML Template")),
        (CSS,  _("CSS Stylesheet")),
        (JS,   _("JS Source File")),
    )

    type   = models.SmallIntegerField(verbose_name=_("File Type"), choices=_FILE_TYPES)
    number = models.SmallIntegerField(verbose_name=_("Number"))
    media  = GenericRelation(MediaFile)

class DeveloperKey(AbstractModel, CreatedModifiedByMixin):
    """
    xxx
    """
    pass

    # name
    # key
    # extend user (non-interactive user)
    # permissions via django auth