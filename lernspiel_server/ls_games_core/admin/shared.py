# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _

from ..models.shared import MediaFile, SourceFile

class MediaFileInline(GenericTabularInline):
    model               = MediaFile
    verbose_name        = _("Media File")
    verbose_name_plural = _("Media Files")

class SourceFileInline(GenericTabularInline):
    model               = SourceFile
    verbose_name        = _("Source File")
    verbose_name_plural = _("Source Files")
