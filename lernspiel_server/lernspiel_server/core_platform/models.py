# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
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
        return "%(app_label)s/%(model)s/%(filename)s" % {
            "app_label": self.content_type.app_label,
            "model":     self.content_type.model,
            "filename":  filename,
        }

    file = models.FileField(verbose_name=_("File"), upload_to=calc_file_path)

    class Meta:
        ordering = ["file"]
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")
    
    def __str__(self):
        return self.file.name

class CustomUser(AbstractUser):
    """
    Replacement for the default Django User model, so that we can distinguish between
    normal human users and remote applications. The first cannot access the web APIs,
    the latter cannot login interactively.
    """
    HUMAN_USER  = 1
    APPLICATION = 2

    _USER_TYPES = (
        (HUMAN_USER,  _("Human User")),
        (APPLICATION, _("Application")),
    )

    user_type = models.SmallIntegerField(verbose_name=_("User Type"), choices=_USER_TYPES, default=HUMAN_USER)

class ApplicationUser(AbstractModel, CreatedModifiedByMixin):
    """
    API Key for remote access to the server by developers or other API clients.
    Developers connect to the server to upload and test new game variants via
    the Game SDK. Other API clients include bots that join games and participate
    one way or another (e.g. as a challenge for students).

    Technically this is an extension to Django's core User model, so that the
    Django permission system can be used to restrict access for API clients.
    But not every User is an Application User.
    """
    DEVELOPER  = 1
    REMOTE_APP = 2

    _KEY_TYPES = (
        (DEVELOPER,  _("Developer Key")),
        (REMOTE_APP, _("Application Key")),
    )

    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="application")
    name        = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    thumbnail   = GenericRelation(MediaFile)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Owner"), on_delete=models.CASCADE, related_name="own_applications")
    key_type    = models.SmallIntegerField(verbose_name=_("Key Type"), choices=_KEY_TYPES)
    api_key     = models.CharField(verbose_name=_("API Key"), max_length=64, editable=False)
    expires     = models.DateTimeField(verbose_name=_("Expires"), null=True, blank=False)
    active      = models.BooleanField(verbose_name=_("Active"), help_text=_("Use this to manually revoke an application without deleting it."))

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

# TODO: Custom auth backend needed? No password for API users?
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#specifying-authentication-backends