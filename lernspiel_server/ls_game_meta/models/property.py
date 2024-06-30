# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.db.models.query   import QuerySet
from django.utils.translation import gettext_lazy as _
from lernspiel_server.utils   import models as db_utils
from .game_component          import GameComponentMeta
from .typed_value             import TypedValueMixin

class PropertyMeta(db_utils.UUIDMixin, TypedValueMixin):
    """
    Named property of a game component. Properties define the state data of a game event.
    They can either be set statically when a game is built or dynamically at runtime through
    the game logic scripts.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="properties")
    
    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Property")
        verbose_name_plural = _("Properties")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class PropertyMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(PropertyMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label