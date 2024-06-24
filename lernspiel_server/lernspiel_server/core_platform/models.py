# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from .db import AbstractModel, CreatedModifiedByMixin
from .utils import hash

class MediaFile(AbstractModel, CreatedModifiedByMixin):
    """
    Generic model to manage uploaded media files. Each file belongs to a model
    like a game type, game or question, using a generic foreign key as defined
    in the built-in `contenttypes` Django app.
    """
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def calc_file_path(self, filename):
        return "%(app_label)s/%(model)s/%(filename)s"

    file = models.FileField(verbose_name=_("File"), upload_to=calc_file_path)

    class Meta:
        ordering = ["file"]
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")
    
    def __str__(self):
        return self.file.name

class ClientApplication(AbstractModel, CreatedModifiedByMixin):
    """
    Remote client application that connects with the server using an API key.
    This is an advanced feature meant to extend the application with bots that
    can join games and act on behalf of a real player. This is probably the
    most useful for open world games, where the bots can navigate on a large
    map to achieve a goal.
    """
    name        = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    thumbnail   = GenericRelation(MediaFile)
    owner       = models.ForeignKey("auth.User", verbose_name=_("Owner"), on_delete=models.CASCADE, related_name="client_applications")
    api_key     = models.CharField(verbose_name=_("API Key"), max_length=64, editable=False)
    expires     = models.DateTimeField(verbose_name=_("Expires"), null=True, blank=False)
    active      = models.BooleanField(verbose_name=_("Active", help_text=_("Use this to manually revoke an application without deleting it.")))

    def __init__(self):
        self.reset_api_key()
    
    def reset_api_key(self, save: bool = False) -> str:
        """
        Calculate new API key and temporarily put it to `self.new_api_key` before
        returning it. Also change `api_key` to the new hashed value.
        """
        self.new_api_key = hash.generate_key(32)
        self.api_key.default = hash.hash_key(self.new_api_key)

        if save:
            self.save()
        
        return self.new_api_key
