# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
import lernspiel_server.utils.models as db_utils
from . import GameComponentMeta

class SlotMeta(db_utils.UUIDMixin):
    """
    Named slot of a game component. Slots define the areas, where a component can embed
    child components. This is very similar to web components that can also have multiple
    named slots where child elements can be inserted.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="slots")
    name   = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)
    
    class Meta:
        verbose_name        = _("Slot")
        verbose_name_plural = _("Slots")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class SlotMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(SlotMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label