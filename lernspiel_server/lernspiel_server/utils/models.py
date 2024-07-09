# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import uuid

from typing                   import Optional
from django.conf              import settings
from django.contrib           import admin
from django.db                import models
from django.db.models         import Q
from django.utils.translation import gettext_lazy as _, get_language
from .                        import hash

class UUIDMixin(models.Model):
    """
    Mixin for models with a UUID primary key instead of Django's default Auto ID
    integer sequence. Since we might often use the IDs in APIs and URLs, for security
    reasons, we want to avoid predictable sequences. But unfortunately we cannot
    enforce this in Django, as Auto IDs needs to be integers.
    """
    id = models.UUIDField(verbose_name=_("Id"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class CreatedModifiedByMixin(models.Model):
    """
    Mixin class for models that shall record the time and user of creation as well as
    the time and user of the last modification.
    """
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Created By"), on_delete=models.SET_DEFAULT, default="", blank=True, null=True)
    created_at  = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Modified By"), on_delete=models.SET_DEFAULT, default="", blank=True, null=True, related_name="+")
    modified_at = models.DateTimeField(verbose_name=_("Modified At"), auto_now=True)

    class Meta:
        abstract = True
    
    @property
    @admin.display(description=_("Last Changed"))
    def created_modified_by(self):
        """
        Get formatted string to display in the Admin or on the website.
        """
        if self.created_by and self.created_at:
            created = _("Created by {created_by} at {created_at}.").format(
                created_by = self.created_by,
                created_at = self.created_at.strftime("%x"),
            )
        elif self.created_by:
            created = _("Created by {created_by}.").format(created_by=self.created_by)
        elif self.created_at:
            created = _("Created at {created_at}.").format(created_at=self.created_at.strftime("%x"))

        if self.modified_by and self.modified_at:
            modified = _("Modified by {modified_by} at {modified_at}.").format(
                modified_by = self.modified_by,
                modified_at = self.modified_at.strftime("%x"),
            )
        elif self.modified_by:
            modified = _("Modified by {modified_by}.").format(modified_by=self.modified_by)
        elif self.modified_at:
            modified = _("Modified at {modified_at}.").format(modified_at=self.modified_at.strftime("%x"))

        if created and modified:
            return "%s %s" % (created, modified)
        elif created:
            return created
        elif modified:
            return modified
        else:
            return ""

class EditKeyMixin(models.Model):
    """
    Mixin class for models that shall have an edit key that can be used by anonymous
    users to regain edit access via a magic link. The key is a 16 character string
    calculated by hashing an UUID. Note that the key itself will not be persistent and
    thus cannot be retrieved later. Only a hash of the key is saved.
    """
    edit_key = models.CharField(verbose_name=_("Edit Key"), max_length=64, editable=False, blank=True)

    class Meta:
        abstract = True

    def reset_edit_key(self, save: bool = False) -> str:
        """
        Calculate a new edit key and return its value. Also set `edit_key` to the hashed
        version to be saved in the database.
        """
        new_edit_key = hash.generate_key(length=16, grouping=4)
        self.edit_key = hash.hash_key(new_edit_key)

        if save:
            self.save()
        
        return new_edit_key

def LanguageField():
    """
    A special model field for language codes. Technically this is a simple foreign key to
    the `Language` model of the core app.
    """
    return models.ForeignKey("lernspiel_server.Language", on_delete=models.CASCADE)

def get_translations(object: models.Model, language: str = "",
                     attr_id: str = "id", attr_translations: str = "translations",
                     attr_t_parent: str = "parent", attr_t_language: str = "language") -> Optional[models.Model]:
    """
    Mixing method to get translations of a model with translations. By default translations are
    stored in a second model, that installs an `translations` ("attr_translations") related attribute.
    The text model usually has the properties `parent` ("attr_t_parent") pointing to the original
    model and `language` ("attr_t_language") with the language code.

    Tries to find translations for the given language (default: language of the current thread)
    or the `LANGUAGE_CODE` setting as fallback, if different.

    Returns the best found translation or None, if none exists.
    """
    if not language:
        language = get_language()
    
    id = getattr(object, attr_id)

    default_language = settings.LANGUAGE_CODE or ""
    default_kwargs   = {attr_t_parent: id, attr_t_language: default_language}
    language_kwargs  = {attr_t_parent: id, attr_t_language: language}

    translations = getattr(object, attr_translations)

    if default_kwargs == language_kwargs:
        results = translations.filter(**language_kwargs);
    else:
        results = translations.filter(Q(**language_kwargs) | Q(**default_kwargs))
   
    if results.count() == 0:
        return None
    elif results.count() == 1:
        return results.first()
    else:
        return results.get(**language_kwargs)

class TranslationMissing(Exception):
    """
    An exception that can be throws, when a translation for something is missing.
    Note, that the `get_translations()` function doesn't throw this exception but
    rather returns `None`.
    """
    pass

def calc_file_path(object, pk, filename):
    """
    Callable for the `upload_to` property of `model.FileField`. Determines the upload bath
    by joining the app label and model name.

    The first parameter normally is the model's `_meta` attribute. But `self.content_type`,
    if it is a `models.ForeignKey` from a generic relation, can make sense to use the app
    name and label of the foreign model, instead.
    """
    model = object.model if type(object) is str else object.model.__name__

    return "%(app_label)s/%(model)s/%(pk)s/%(filename)s" % {
        "app_label": object.app_label,
        "model":     model,
        "filename":  filename,
    }