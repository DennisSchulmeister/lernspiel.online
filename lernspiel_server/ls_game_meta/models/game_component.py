# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from typing                             import Optional
from django.contrib.contenttypes.fields import GenericRelation
from django.db                          import models
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from lernspiel_server.models            import MediaFile, SourceFile
from .category                          import Category

class GameComponentMeta(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    Meta description of a game component, the main building block for games.
    """
    # General information
    def _calc_file_path(self, filename):
        return db_utils.calc_file_path(self._meta, filename)
    
    name       = models.CharField(verbose_name=_("Name"), max_length=255, unique=True)
    category   = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail  = models.FileField(verbose_name=_("Thumbnail"), upload_to=_calc_file_path, null=True, blank=True)

    # Source files
    media_files  = GenericRelation(MediaFile)
    source_files = GenericRelation(SourceFile)

    # Django meta information
    class Meta:
        verbose_name        = _("Game Component")
        verbose_name_plural = _("Game Components")
        ordering            = ["category", "name"]
        indexes             = [models.Index(fields=["name"])]
    
    def __str__(self):
        return self.name

    # Translated texts
    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

class GameComponentMeta_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent      = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="translations")
    label       = models.CharField(verbose_name=_("Label"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass
    