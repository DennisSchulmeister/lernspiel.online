# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from .db import AbstractModel

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class MediaFile(AbstractModel):
    """
    Generic model to manage uploaded media files. Each file belongs to a model
    like a game type, game or question, using a generic foreign key as defined
    in the built-in `contenttypes` Django app.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def calc_file_path(self, filename):
        return "%(app_label)s/%(model)s/%(filename)s"

    file = models.FileField(verbose_name=_("File"), upload_to=calc_file_path)

    class Meta:
        ordering = ["file"]
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")
    
    def __str__(self):
        return self.file.name