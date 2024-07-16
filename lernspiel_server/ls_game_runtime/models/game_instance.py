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

# TODO: This is currently a stub. Full implementation needed. :-)
class GameInstance(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    Possibly running instance of a game. This is the result of someone starting the game
    to create an invite code. The invite code is simply the ID of this table. Latest when
    a participant joins, one of the game runner instances will pick up the game from here,
    execute the server-side game logic and update this table periodically to persist the
    game state and signal that it is still alive.
    """
    # Game definition and state
    definition     = models.ForeignKey(GameDefinition, on_delete=models.CASCADE, verbose_name=_("Game Definition"))
    max_inactivity = models.SmallIntegerField(verbose_name=_("Max. Inactivity Minutes"), default=1, blank=True, help_text=_("Game execution will stop if no participant joins within this period. The game will be resumed once a participant joins. Zero means to never stop."))

    # Game Runner status
    running   = models.BooleanField(verbose_name=_("Currently Running"))
    channel   = models.CharField(verbose_name=_("Channel"), max_length=255, blank=True)
    heartbeat = models.DateTimeField(verbose_name=_("Heartbeat"), blank=True, null=True)

    participants_count = models.IntegerField(verbose_name=_("Current Participants"), default=0, blank=True)
    participants_since = models.DateTimeField(verbose_name=_("Last Join or Leave"), blank=True, null=True)

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
        return "%s (%s)" % (self.definition.name, self.id)
    
    @property
    @admin.display(ordering="definition__name", description=_("Game Definition"))
    def definition_name(self):
        return self.definition.name