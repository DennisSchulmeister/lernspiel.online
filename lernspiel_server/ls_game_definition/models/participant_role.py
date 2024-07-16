# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _
from lernspiel_server.utils   import models as db_utils
from .game_definition         import GameDefinition

class ParticipantRole(db_utils.UUIDMixin):
    """
    Games support different participant roles e.g. to distinguish student players from
    the teacher controlling the game. Each game must have at least one participant role.
    Each role then gets its own Game ID with which participants can join the game.
    """
    parent = models.ForeignKey(GameDefinition, on_delete=models.CASCADE, related_name="participant_roles")
    name   = models.CharField(verbose_name=_("Name"), max_length=255)
    limit  = models.SmallIntegerField(verbose_name=_("Max. Allowed Participants"), default=0, blank=True)

    class Meta:
        verbose_name        = _("Participant Role")
        verbose_name_plural = _("Participant Roles")
        ordering            = ["name"]
        indexes             = [models.Index(fields=["name"])]
    
    def __str__(self):
        return self.name

class ParticipantRole_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(ParticipantRole, on_delete=models.CASCADE, related_name="translations")
    label  = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass