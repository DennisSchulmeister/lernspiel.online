# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _

class TypedValueMixin(models.Model):
    """
    Mixin for properties and parameters which define typed data values.
    """
    PLAIN_TEXT     = "plain"
    FORMATTED_TEXT = "text"
    NUMBER         = "num"
    BOOL           = "bool"
    DICTIONARY     = "dict"

    _DATA_TYPES = {
        PLAIN_TEXT:     _("Plain Text"),
        FORMATTED_TEXT: _("Formatted Text"),
        NUMBER:         _("Number"),
        BOOL:           _("Boolean"),
        DICTIONARY:     _("Dictionary"),
    }

    name      = models.CharField(verbose_name=_("Name"), max_length=100)
    data_type = models.CharField(verbose_name=_("Data Type"), max_length=10, choices=_DATA_TYPES)
    length    = models.PositiveSmallIntegerField(verbose_name=_("Length"), null=True, blank=True)
    is_array  = models.BooleanField(verbose_name=_("Is Array"))

    class Meta:
        abstract = True