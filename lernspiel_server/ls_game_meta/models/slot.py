# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from typing                   import Optional
from django.db                import models
from django.utils.translation import gettext_lazy as _
from lernspiel_server.utils   import models as db_utils
from .game_component          import GameComponentMeta

class SlotMeta(db_utils.UUIDMixin):
    """
    Named slot of a game component. Slots define the areas, where a component can embed
    child components. This is very similar to web components that can also have multiple
    named slots where child elements can be inserted.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="slots")
    name   = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)
   
    class Meta:
        verbose_name        = _("Slot")
        verbose_name_plural = _("Slots")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

class SlotMeta_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(SlotMeta, on_delete=models.CASCADE, related_name="translations")
    label  = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass