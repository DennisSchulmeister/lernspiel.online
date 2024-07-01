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
from lernspiel_server.models            import MediaFile
from .formatted_content_mixin           import FormattedContentMixin

class Snippet(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    A reusable text snippet which can be used inside text pages and templates.
    Inside text pages `{snippet foobar}` must be used. For templates there's a
    similar template tag:

    ```html
    {% load snippet %}
    {% snippet foobar %}
    ```
    """
    name        = models.CharField(_("Name"), max_length=64, blank=False, null=False, unique=True)
    media_files = GenericRelation(MediaFile)

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)
    
    class Meta:
        verbose_name        = _("Snippet")
        verbose_name_plural = _("Snippets")
        ordering            = ["name"]

        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

class Snippet_T(db_utils.UUIDMixin, FormattedContentMixin):
    parent   = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name="translations")
    language = db_utils.LanguageField()

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]

    def __str__(self):
        if len(self.content) > 50:
            return "%s…" % self.content
        else:
            return self.content
