# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
import lernspiel_server.utils.models as db_utils
from . import EventMeta, TypedValueMixin

class EventParameterMeta(db_utils.UUIDMixin, TypedValueMixin):
    """
    Named event parameter of an event. These are parameters that are passed to event subscribers.
    They share the same semantics than game component properties but are temporary and only bound
    to a single event occurrence.
    """
    parent = models.ForeignKey(EventMeta, on_delete=models.CASCADE, related_name="parameters")

    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Parameter")
        verbose_name_plural = _("Parameters")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class EventParameterMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(EventParameterMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label