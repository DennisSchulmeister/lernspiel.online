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
from typing                   import Optional

class Category(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    Hierarchical categories for game components. These define a directory-like
    structure to cluster related components and make them easier to find in
    the game editor UI.
    """
    name     = models.CharField(verbose_name=_("Name"), max_length=255)
    parent   = models.ForeignKey("self", verbose_name=_("Parent Category"), on_delete=models.CASCADE, null=True, blank=True)
    position = models.SmallIntegerField(verbose_name=_("Position"))
   
    class Meta:
        verbose_name        = _("Category")
        verbose_name_plural = _("Categories")
        ordering            = ["position"]      # "parent" -> Infinite loop caused by ordering.
        
        indexes = [
            models.Index(fields=["parent", "position"]),
            models.Index(fields=["parent", "name"]),
        ]

    def __str__(self):
        return self.name

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

class Category_T(db_utils.UUIDMixin, db_utils.TranslatableMixin):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="translations")
    label  = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass
