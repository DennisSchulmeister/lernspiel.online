# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators             import MaxValueValidator
from django.db                          import models
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from lernspiel_server.models            import MediaFile

class Background(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    A collection of background images that will be randomly shown.
    """
    name          = models.CharField(_("Name"), max_length=255, blank=False)
    media_files   = GenericRelation(MediaFile)
    overlay_color = models.CharField(_("Overlay Color"), max_length=7, blank=True, default="", help_text="Hexadecimal CSS color code")
    overlay_alpha = models.PositiveSmallIntegerField(_("Overlay Opacity %"), help_text=_("Between 0 and 100, 0 = fully transparent"), default=0, validators=[MaxValueValidator(100)])
    blur          = models.PositiveSmallIntegerField(_("Blur %"), help_text=_("Between 0 and 100, 0 = no blur"), default=0, validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name        = _("Background")
        verbose_name_plural = _("Backgrounds")
        ordering            = ["name"]
        indexes             = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name
    