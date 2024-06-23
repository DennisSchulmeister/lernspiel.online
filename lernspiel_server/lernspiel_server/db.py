# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import hashlib, uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class AbstractModel(models.Model):
    """
    Abstract base class for all models. Makes sure that the model uses a UUID
    primary key, because the auto ID fields from Django can only use integer
    sequences. However, for security reasons, as we are using the IDs in our
    URLs, we don't want to have sequential IDs.

    Additionally adds fields for who created or changed the entry when.
    """
    id          = models.UUIDField(verbose_name=_("Id"), primary_key=True, default=uuid.uuid4, editable=False)
    created_by  = models.ForeignKey(User, verbose_name=_("Created By"), on_delete=models.SET_DEFAULT, default="", blank=True)
    created_at  = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    modified_by = models.ForeignKey(User, verbose_name=_("Modified By"), on_delete=models.SET_DEFAULT, default="", blank=True, related_name="+")
    modified_at = models.DateTimeField(verbose_name=_("Modified At"), auto_now=True)

    class Meta:
        abstract = True

class EditKeyMixin:
    """
    Mixin class for models that shall have an edit key that can be used by anonymous
    users to regain edit access via a magic link. The key is a 16 character string
    calculated by hashing an UUID. Note that the key itself will not be persistent and
    thus cannot be retrieved later. Only a hash of the key is saved.
    """

    def __init__(self):
        self.new_edit_key = hashlib.shake_128(uuid.uuid4().bytes).hexdigest(16)
        self.edit_key.default = "shake_128:16:%s" % hashlib.shake_128(self.new_edit_key).hexdigest(16)
    
    edit_key = models.CharField(verbose_name=_("Edit Key"), max_length=32, editable=False)