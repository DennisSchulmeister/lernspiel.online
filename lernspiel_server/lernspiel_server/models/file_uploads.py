# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils import models as db_utils

class AbstractFileModel(db_utils.UUIDMixin):
    """
    Abstract base class for the generic file upload models below. Contains the common
    fields and functionality like a generic relation to the owner model and fields for
    the file data and meta data.
    """
    # Link to related model
    def _calc_file_path(self, filename):
        return db_utils.calc_file_path(self.content_type, self.id, filename)
    
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Uploaded file data
    file_data = models.FileField(verbose_name=_("File Data"), upload_to=_calc_file_path)
    file_name = models.CharField(verbose_name=_("File Name"), max_length=255)
    file_size = models.PositiveIntegerField(verbose_name=_("File Size"), null=True)
    mime_type = models.CharField(verbose_name=_("MIME Type"), max_length=64)

    # Django meta information
    class Meta:
        abstract = True
        ordering = ["content_type", "object_id", "file_name"]

        indexes = [
            models.Index(fields=["content_type", "object_id", "file_name"])
        ]

    def __str__(self):
        return self.file.name

class MediaFile(AbstractFileModel):
    """
    Generic model for media files, when a model can have multiple media files like
    images or sounds that shall later be accessed by their file name. To use this
    model simply add a `GenericRelation` to the model that shall have media files.
    """
    class Meta(AbstractFileModel.Meta):
        verbose_name        = _("Media File")
        verbose_name_plural = _("Media Files")

class SourceFile(AbstractFileModel):
    """
    Generic model for source files, when a model can have multiple source files for
    execution on frontend or backend. This can be HTML/CSS/JavaScript on the frontend
    or GameScript for game logic on the backend. To use this model simply add a
    `GenericRelation` to the model that can shall have source files.
    """
    # Source file data
    HTML   = "html"
    CSS    = "css"
    JS     = "js"
    SCRIPT = "script"

    _FILE_TYPES = {
        HTML:   _("HTML Template"),
        CSS:    _("CSS Stylesheet"),
        JS:     _("JS Source File"),
        SCRIPT: _("Game Script"),
    }

    source_type = models.CharField(verbose_name=_("Source Type"), max_length=10, choices=_FILE_TYPES)
    position    = models.SmallIntegerField(verbose_name=_("Sort Order"))

    # Django meta information
    class Meta(AbstractFileModel.Meta):
        verbose_name        = _("Source File")
        verbose_name_plural = _("Source Files")
        ordering            = ["content_type", "object_id", "source_type", "position"]

        indexes = AbstractFileModel.Meta.indexes + [
            models.Index(fields=["content_type", "object_id", "source_type", "position"])
        ]
        
    def __str__(self):
        file_name  = self.source_file.name if self.source_file else ""

        return "{source_type} ({position}): {file_name}".format(
            source_type = self.source_type,
            position    = self.position,
            file_name   = file_name
        )