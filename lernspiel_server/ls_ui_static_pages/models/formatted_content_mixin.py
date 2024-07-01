# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _
from markdown                 import markdown
from ..custom_tags.tag_parser import replace_tags

class FormattedContentMixin(models.Model):
    """
    Mixin model class for models with formatted text content. Allows to choose one of
    several formats which can always be rendered into HTML.
    """
    PLAIN    = "plain"
    HTML     = "html"
    MARKDOWN = "markdown"

    _FORMATS = {
        PLAIN:    _("Plain Text"),
        HTML:     _("HTML"),
        MARKDOWN: _("Markdown"),
    }

    format  = models.CharField(_("Format"), max_length=10, choices=_FORMATS)
    content = models.TextField(_("Content"), blank=True, null=False)

    class Meta:
        abstract = True
    
    def get_html(self) -> str:
        """
        Get HTML formatted content ready for display. Compiles the format into HTML and
        replaces all custom tags inside.
        """
        html = str(self.content)

        match self.format:
            case self.PLAIN:
                html = html.replace("&", "&amp;")
                html = html.replace("<", "&lt;")
                html = html.replace(">", "&gt;")
                return html
            case self.MARKDOWN:
                html = markdown(html)
        
        return replace_tags(html, self.parent)
