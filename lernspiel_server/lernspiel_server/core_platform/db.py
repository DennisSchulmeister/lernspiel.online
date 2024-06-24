# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import hash

class AbstractModel(models.Model):
    """
    Abstract base class for all models. Makes sure that the model uses a UUID
    primary key, because the auto ID fields from Django can only use integer
    sequences. However, for security reasons, as we are using the IDs in our
    URLs, we don't want to have sequential IDs.
    """
    id = models.UUIDField(verbose_name=_("Id"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class CreatedModifiedByMixin:
    """
    Mixin class for models that shall record the time and user of creation as well as
    the time and user of the last modification.
    """
    created_by  = models.ForeignKey(User, verbose_name=_("Created By"), on_delete=models.SET_DEFAULT, default="", blank=True)
    created_at  = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified By"), on_delete=models.SET_DEFAULT, default="", blank=True, related_name="+")
    modified_at = models.DateTimeField(verbose_name=_("Modified At"), auto_now=True)

class EditKeyMixin:
    """
    Mixin class for models that shall have an edit key that can be used by anonymous
    users to regain edit access via a magic link. The key is a 16 character string
    calculated by hashing an UUID. Note that the key itself will not be persistent and
    thus cannot be retrieved later. Only a hash of the key is saved.
    """

    edit_key = models.CharField(verbose_name=_("Edit Key"), max_length=64, editable=False)

    def __init__(self):
        self.reset_edit_key()

    def reset_edit_key(self, save: bool = False) -> str:
        """
        Calculate new edit key and temporarily put it to `self.new_edit_key` before
        returning it. Also change `edit_key` to the new hashed value.
        """
        self.new_edit_key = hash.generate_key(16)
        self.edit_key.default = hash.hash_key(self.new_edit_key)

        if save:
            self.save()
        
        return self.new_edit_key