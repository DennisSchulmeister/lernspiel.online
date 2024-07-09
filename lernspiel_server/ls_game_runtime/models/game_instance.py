# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib                            import admin
from django.db                                 import models
from django.utils.translation                  import gettext_lazy as _
from lernspiel_server.utils                    import models as db_utils
from ls_game_definition.models.game_definition import GameDefinition
from lernspiel_server.utils.hash               import generate_key


# TODO: This is currently a stub. Full implementation needed. :-)
class GameInstance(db_utils.CreatedModifiedByMixin):
    """
    Abstract definition of a game. This is what game authors work with in the game builder.
    It defines the component structure, rules and additional source files of the game.
    The game runtime uses these internally when executing the game instances.
    """
    def _generate_game_id():
        return generate_key(length=12, grouping=4)
    
    # Game state
    id         = models.CharField(verbose_name=_("Game ID"), max_length=64, primary_key=True, default=_generate_game_id, editable=False)
    definition = models.ForeignKey(GameDefinition, on_delete=models.CASCADE, verbose_name=_("Game Definition"))

    # Game Runner status
    running   = models.BooleanField(verbose_name=_("Running"))
    channel   = models.CharField(verbose_name=_("Channel"), max_length=255, blank=True)
    heartbeat = models.DateTimeField(verbose_name="Heartbeat", blank=True)

    # Django meta information
    class Meta:
        verbose_name        = _("Game Instance")
        verbose_name_plural = _("Game Instances")
        ordering            = ["definition", "created_at"]

        indexes = [
            models.Index(fields=["definition", "running"]),
            models.Index(fields=["running", "channel"]),
            models.Index(fields=["channel", "running"]),
        ]

    def __str__(self):
        return self.id
    
    @property
    @admin.display(ordering="definition__name", description=_("Game Definition"))
    def definition_name(self, obj):
        return obj.definition.name