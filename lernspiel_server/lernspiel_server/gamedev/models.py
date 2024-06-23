# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from ..db import AbstractModel
from ..models import MediaFile

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

class GameType(AbstractModel):
    """
    Definition of a game type like "Quiz Show", "Pot of Luck" and so on. This defines
    the capabilities and game mechanics of a game as well as how to render its content.
    Rendering uses two embedded JavaScript and CSS files that can be uploaded or linked
    from a different source.
    """
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    library_js_src = models.CharField(verbose_name=_("JavaScript Source"), max_length=255)
    library_css_src = models.CharField(verbose_name=_("CSS Source"), max_length=255, blank=True)
    media_files = GenericRelation(MediaFile)

    # Supported question types, max answers per xChoice question, WHAT ELSE???

    class Meta:
        ordering = ["name"]
        verbose_name = _("Game Type")
        verbose_name_plural = _("Game Types")
    
        indexes = [
            models.Index(["name"]),
        ]

    def __str__(self):
        return self.name
