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
from django.utils import timezone

from ....core_platform.db import AbstractModel, CreatedModifiedByMixin, EditKeyMixin
from ....core_platform.models import MediaFile
from . import GameType, GameVariant

class GameDefinition(AbstractModel, CreatedModifiedByMixin, EditKeyMixin):
    """
    xxx
    """
    # content type for inheritance

    name    = models.CharField(verbose_name=_("Name"), max_length=255)
    type    = models.ForeignKey(GameType, verbose_name=_("Type"), on_delete=models.CASCADE)
    variant = models.ForeignKey(GameVariant, verbose_name=_("Variant"), on_delete=models.CASCADE)
    media   = GenericRelation(MediaFile)

    description = models.TextField(verbose_name=_("Description"), blank=True)
    last_access = models.DateTimeField(verbose_name=_("Last Access"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
    
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["last_access", "id"])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # TODO
        return ""
    
    def touch(self, save):
        """
        Update the last access timestamp and optionally save the change.
        """
        self.last_access = timezone.now()
        self.save() if save else None

class GameElement(AbstractModel, CreatedModifiedByMixin):
    """
    xxx
    """
    media = GenericRelation(MediaFile)
    
    # content type for inheritance
    # name
    # state = START, RUNNING, END
    # order
    # background (CSS?)

class TextPanelElement(GameElement):
    """
    A simple non-interactive game element that simply shows some textual information
    before the game continues.
    """
    text = models.TextField(verbose_name=_("Text"))