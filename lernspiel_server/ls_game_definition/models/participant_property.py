# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from typing                          import Optional
from django.db                       import models
from django.utils.translation        import gettext_lazy as _
from lernspiel_server.utils          import models as db_utils
from ls_game_meta.models.typed_value import TypedValueMixin
from .participant_role               import ParticipantRole

class ParticipantProperty(db_utils.UUIDMixin, TypedValueMixin):
    """
    Typed property associated with specific participants of a game. This is usually used
    to assign a score value to players, but it is flexible enough to cove more complex
    use-cases, too.
    """
    parent = models.ForeignKey(ParticipantRole, on_delete=models.CASCADE, related_name="parameters")

    class Meta:
        verbose_name        = _("Participant Property")
        verbose_name_plural = _("Participant Properties")
        # ordering            = ["parent", "name"],        # Makes the Django Admin crash?!
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

class ParticipantProperty_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(ParticipantProperty, on_delete=models.CASCADE, related_name="translations")
    label  = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass