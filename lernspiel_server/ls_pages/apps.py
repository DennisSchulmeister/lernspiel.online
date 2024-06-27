# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PagesConfig(AppConfig):
    """
    Pages App: Manages flat text pages and the site navigation menu.
    The idea is similar to Django's built-in flatpages app, but pages can
    be translated and navigation menus can be defined.
    """
    name         = "ls_pages"
    verbose_name = _("Pages")
