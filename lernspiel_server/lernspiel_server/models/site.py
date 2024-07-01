# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils.models import calc_file_path

class Site(models.Model):
    """
    Extended version of Django's built-in Site model that additionally allows to
    upload a logo.
    """
    # Basic site data
    id     = models.PositiveIntegerField(verbose_name=_("Id"), primary_key=True, editable=True)
    domain = models.CharField(verbose_name=_("Domain Name"), max_length=100)
    name   = models.CharField(verbose_name=_("Display Name"), max_length=255)

    # Logo image
    def _calc_file_path(self, filename):
        return calc_file_path(self._meta, self.id, filename)
    
    logo = models.FileField(verbose_name=_("Logo Image"), upload_to=_calc_file_path)

    # Theming values
    logo_width = models.CharField(verbose_name=_("Logo Width"), max_length=20, default="20em")
    header_bg  = models.CharField(verbose_name=_("Header Background"), max_length=100, default="#234769")
    link_color = models.CharField(verbose_name=_("Link Color"), max_length=20, default="crimson")

    # Django meta information
    class Meta:
        verbose_name        = _("Website")
        verbose_name_plural = _("Websites")

    def __str__(self):
        return self.name