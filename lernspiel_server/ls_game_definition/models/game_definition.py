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

# TODO: This is currently a stub. Full implementation needed. :-)
class GameDefinition(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin, db_utils.EditKeyMixin):
    """
    Abstract definition of a game. This is what game authors work with in the game builder.
    It defines the component structure, rules and additional source files of the game.
    The game runtime uses these internally when executing the game instances.
    """
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    class Meta:
        verbose_name        = _("Game Definition")
        verbose_name_plural = _("Game Definitions")
        ordering            = ["name"]
        indexes             = [models.Index(fields=["name"])]
    
    def __str__(self):
        return self.name
