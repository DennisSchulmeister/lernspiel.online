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

class EventMeta(db_utils.UUIDMixin):
    """
    Named event of a game component. Game components emit events to trigger game logic, e.g.
    when a button is pressed or a timeout expires. Game logic scripts can subscribe to these
    events to update the game state by setting property values of the game components.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="events")
    name   = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Event")
        verbose_name_plural = _("Events")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class EventMeta_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(EventMeta, on_delete=models.CASCADE, related_name="translations")
    label  = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass