# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime                      import date
from django.conf                   import settings
from django.utils.translation      import gettext_lazy as _
from lernspiel_server.utils.models import calc_file_path, TranslationMissing
from .tag_parser                   import context_stack
from .                             import tag_registry
from ..                            import models

def file_url(tagname: str, url: str = "") -> str:
    """
    Custom tag to use static files in text pages and snippets. This allows to address
    the static files managed by Django, that would otherwise also be used in templates.
    Wants a file name is its single parameter:
    
     * `{static image.jpg}` to access files from `STATIC_URL`
     * `{media image.jpg}` to access files from `MEDIA_URL`
    """
    if tagname == "static":
        prefix = settings.STATIC_URL if hasattr(settings, "STATIC_URL") else ""
    elif tagname == "media":
        prefix = settings.MEDIA_URL if hasattr(settings, "MEDIA_URL") else ""

    if prefix.endswith("/"):
        prefix = prefix[:-1]

    if not url:
        return prefix
    else:
        return "%s/%s" % (prefix, url)

tag_registry.register(
    name    = "static",
    example = "{static image.png}",
    help    = _("Insert URL of a static file from the server"),
    func    = file_url,
)

tag_registry.register(
    name    = "media",
    example = "{media default_logo.svg}",
    help    = _("Insert URL of an uploaded media file from server"),
    func    = file_url,
)

@tag_registry.register(
    name    = "attachment",
    example = "{attachment uploaded_image.png}",
    help    = _("Insert URL of a media file attached to the current page or snippet"),
)
def attachment(tagname: str, filename: str) -> str:
    """
    Insert URL of an attached media into the page. Depending in where the custom tag is
    used, the media file must be uploaded to the text page or snippet. It is assumed,
    that the page or snippet use the `calc_file_path()` function during upload to find
    the storage location, and that hey have an `id` field.
    """
    model = context_stack[-1]
    return calc_file_path(model._meta, model.id, filename)

@tag_registry.register(
    name    = "snippet",
    example = "{snippet imprint}",
    help    = _("Insert the content of a text snippet"),
)
def snippet(tagname: str, snippet_name: str = "") -> str:
    """
    Custom tag handler to insert a named snipped into the page. Raises `Snippet.DoesNotExist`
    or `TranslationMissing` when debug mode is active. In production the errors will be silently
    ignored and an empty string returned.
    """
    try:
        snippet = models.Snippet.objects.get(pk=snippet_name)
        translations = snippet.get_translations()

        if translations:
            return translations.get_htm()
        elif settings.DEBUG:
            raise TranslationMissing
        else:
            return ""
    except models.Snippet.DoesNotExist:
        if settings.DEBUG:
            raise
        else:
            return ""

@tag_registry.register(
    name    = "mailto",
    example = _('<a href="{mailto test@example.com}">Send e-mail</a>'),
    help    = _("Hide e-mail address from spammers")
)
def mailto(tagname: str, email: str = "", quote='"') -> str:
    """
    This function is a python version of the `encode_adress(email)` javascript
    function. All it does is to shift all uneven characters by one place and
    all even characters by two places. Only printable ascii characters between
    code point 33 and 127 are shifted.

    The returned string must be inserted into the href-attribute of an link.
    By default it is assumed that the attribute value is surrounded by double
    quotes like this: `<a href="{mailto test@example.com}">`. If single quotes
    are used, they can be declared as `<a href='{mailto test@example.com' "'"}'>`
    """
    email = email.encode("ascii", "ignore")

    encoded = ""
    change = True

    for char in email:
        change = not change
        code = ord(char)

        if not change:
            if code >= 33 and code <= 126:
                code += 1
            elif code == 127:
                code = 33
        else:
            if code >= 33 and code <= 125:
                code += 2
            elif code == 126:
                code = 33
            elif code == 127:
                code = 34

        encoded += chr(code)

    return "javascript:decode_and_link_to(%s%s%s)" % (quote, encoded, quote)

@tag_registry.register(
    name    = "date",
    example = _("{date} or {date %%Y-%%m-%%d}"),
    help    = _("Hide e-mail address from spammers")
)
def date(tagname: str, formatstring: str = "%x") -> str:
    """
    Insert current date into page. The formatstring must contain any option
    accepted by Python's `date.strftime()` method.
    """
    return date.today().strftime(formatstring)