# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                                  import models
from django.utils.translation                   import gettext_lazy as _
from lernspiel_server.utils                     import models as db_utils
from lernspiel_server.utils.hash                import generate_key
from ls_game_definition.models.participant_role import ParticipantRole
from ..models.game_instance                     import GameInstance

class GameId(db_utils.UUIDMixin):
    """
    Game ID that participants use to join a game instance with a particular role.
    """
    def _generate_game_id():
        return generate_key(length=12, grouping=6)
    
    id               = models.CharField(verbose_name=_("Game ID"), max_length=64, primary_key=True, default=_generate_game_id, editable=False)
    game_instance    = models.ForeignKey(GameInstance, on_delete=models.CASCADE, verbose_name=_("Game Instance"))
    participant_role = models.ForeignKey(ParticipantRole, on_delete=models.CASCADE, verbose_name=_("Participant Role"))

    # Django meta information
    class Meta:
        verbose_name        = _("Game ID")
        verbose_name_plural = _("Game IDs")
        ordering            = ["id"]

    def __str__(self):
        return self.id