# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from lernspiel_server.db import AbstractModel, CreatedModifiedByMixin
from lernspiel_server.models import MediaFile

class GameVariant(AbstractModel, CreatedModifiedByMixin):
    """
    Concrete variant of a game type defining the appearance and overall rule set of
    the game. A game type could be "Quiz" as implemented by the corresponding Django app.
    Game variants could then be "TV Show", "Questionnaire" etc.

    Game variants contain multiple media files and source files that are loaded by the
    frontend to be executed in the web browser. Developers can use the Game SDK to build,
    test and deploy new game variants.
    """
    name        = models.CharField(verbose_name=_("Name"), max_length=255)
    game_type   = models.CharField(verbose_name=_("Game Type"), max_length=64)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    media       = GenericRelation(MediaFile)

    # Link to settings for the concrete game type
    par_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    par_object_id    = models.UUIDField()
    parameters       = GenericForeignKey("par_content_type", "par_object_id")

    class Meta:
        verbose_name        = _("Game Variant")
        verbose_name_plural = _("Game Variants")
        ordering            = ["name"]
        
    def __str__(self):
        return self.name

class SourceFile(AbstractModel, CreatedModifiedByMixin):
    """
    Client-side source file for a game variant. Will be loaded in each participant's browser
    in the order indicated by the sort number.
    """
    HTML = 1
    CSS  = 2
    JS   = 3

    _FILE_TYPES = {
        HTML: _("HTML Template"),
        CSS:  _("CSS Stylesheet"),
        JS:   _("JS Source File"),
    }

    game_variant = models.ForeignKey(GameVariant, on_delete=models.CASCADE, editable=False)
    file_type    = models.SmallIntegerField(verbose_name=_("File Type"), choices=_FILE_TYPES)
    sort_order   = models.SmallIntegerField(verbose_name=_("Sort Order"))
    media        = GenericRelation(MediaFile)

    class Meta:
        verbose_name        = _("Source File")
        verbose_name_plural = _("Source Files")
        ordering            = ["file_type", "sort_order"]
        
    def __str__(self):
        media_file = self.media.all()[0]
        file_name  = media_file.name if media_file is not None else ""

        return "{file_type} ({sort_order}): {file_name}".format(
            file_type  = self.file_type,
            sort_order = self.sort_order,
            file_name  = file_name
        )
