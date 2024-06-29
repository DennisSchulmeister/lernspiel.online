# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from lernspiel_server.db import AbstractModel, CreatedModifiedByMixin
from .shared import MediaFile, SourceFile

class GameComponentMeta(AbstractModel, CreatedModifiedByMixin):
    """
    Concrete variant of a game type defining the appearance and overall rule set of
    the game. A game type could be "Quiz" as implemented by the corresponding Django app.
    Game variants could then be "TV Show", "Questionnaire" etc.

    Game variants contain multiple media files and source files that are loaded by the
    frontend to be executed in the web browser. Developers can use the Game SDK to build,
    test and deploy new game variants.
    """
    # TODO :-)
    name         = models.CharField(verbose_name=_("Name"), max_length=255)
    description  = models.TextField(verbose_name=_("Description"), blank=True)

    media_files  = GenericRelation(MediaFile)
    source_files = GenericRelation(SourceFile)

    # Django meta information
    class Meta:
        verbose_name        = _("Game Component")
        verbose_name_plural = _("Game Components")
        ordering            = ["name"]

        indexes = [
            models.Index(fields=["name"]),
        ]
        
    def __str__(self):
        return self.name

