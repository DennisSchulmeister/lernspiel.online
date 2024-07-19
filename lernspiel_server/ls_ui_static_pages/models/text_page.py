# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime                           import date
from typing                             import Optional
from django.contrib                     import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.db                          import models
from django.urls                        import reverse
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils
from lernspiel_server.models            import MediaFile
from .background                        import Background
from .custom_css                        import CustomCSS
from .formatted_content_mixin           import FormattedContentMixin
from .menu_assignment                   import MenuAssignment
from .page_type                         import PageType

class TextPage(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    An extended version of Django flat pages with the following extras:

      * Translations
      * Publishing status
      * Date-based publishing of pages
      * A "show title on page" flag
      * Attached media files
      * Custom tags
      * Reusable text snippets
      * Page Types
      * Menus
      * Custom CSS
    """
    # General information
    url         = models.CharField(verbose_name=_("URL"), max_length=255)
    name        = models.CharField(verbose_name=_("Name"), max_length=255)
    page_type   = models.ForeignKey(PageType, verbose_name=_("Page Type"), on_delete=models.SET_NULL, null=True)

    # Page Content
    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)
    
    show_title  = models.BooleanField(verbose_name=_("Show title on page"), default=True, null=False)
    background  = models.ForeignKey(Background, verbose_name=_("Background"), on_delete=models.SET_NULL, null=True, blank=True)
    media_files = GenericRelation(MediaFile)
    custom_css  = GenericRelation(CustomCSS)
    menus       = GenericRelation(MenuAssignment, help_text=_("Use this to override the menu assignments from the page type."))
    
    # Publishing status
    login_required = models.BooleanField(verbose_name=_("Login Required"), default=False)
    published      = models.BooleanField(verbose_name=_("Publish Page"), default=False, null=False)
    publish_start  = models.DateField(verbose_name=_("Publish On"), blank=True, null=True)
    publish_end    = models.DateField(verbose_name=_("Publish Until"), blank=True, null=True)

    # Django meta information
    class Meta:
        verbose_name        = _("Text Page")
        verbose_name_plural = _("Text Pages")
        ordering            = ["url",]

        indexes = [
            models.Index(fields=["url"])
        ]

    def __str__(self):
        return "%s: %s" % (self.url, self.name)

    # Custom methods
    def get_absolute_url(self):
        return self.get_preview_url()

    def get_preview_url(self):
        return reverse("textpage-preview", kwargs={"url": str(self.url)})

    def get_published_url(self):
        return reverse("textpage", kwargs={"url": str(self.url)})

    @property
    @admin.display(description=_("Page is published"), boolean=True)
    def is_published(self):
        today = date.today()

        if not self.published:
            return False
        elif self.publish_start and self.publish_start > today:
            return False
        elif self.publish_end and self.publish_end < today:
            return False
        else:
            return True

class TextPage_T(db_utils.UUIDMixin, db_utils.TranslatableMixin, FormattedContentMixin):
    parent = models.ForeignKey(TextPage, on_delete=models.CASCADE, related_name="translations")
    title  = models.CharField(verbose_name=_("Title"), max_length=255)

    class Meta(db_utils.TranslatableMixin.Meta):
        pass