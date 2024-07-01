# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericRelation
from django.db                          import models
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from lernspiel_server.models            import MediaFile

class Background(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    A collection of background images that will be randomly shown.
    """
    name        = models.CharField(_("Name"), max_length=255, blank=False)
    media_files = GenericRelation(MediaFile)

    class Meta:
        verbose_name        = _("Background")
        verbose_name_plural = _("Backgrounds")
        ordering            = ["name"]

        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name