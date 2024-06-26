# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django import template
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .context_processors import site
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

class User(AbstractUser):
    """
    Extension to Django's core User model to allow non-human application users
    that connect via API to the server. Application users use a username with 
    pre-defined password (the API Key). Developers use this to connect their
    local machine to the server via the Game SDK. Bots and other applications
    join games to participate. Besides that there are regular users logging in
    on the website.

    `AbstractUser` already contains the following fields:

     - username (key)
     - first_name
     - last_name
     - email
     - is_staff
     - is_active
     - date_joined

    Developers and Applications need an e-mail address to which the API Key
    can be sent. Applications also use the field `first_name` to save the
    clear-text name of the application.
    """
    REGULAR_USER = 0
    DEVELOPER    = 1
    APPLICATION  = 2

    _USER_TYPES = {
        REGULAR_USER: _("Regular User"),
        DEVELOPER:    _("Developer"),
        APPLICATION:  _("Application")
    }

    user_type    = models.SmallIntegerField(verbose_name=_("User Type"), choices=_USER_TYPES, default=REGULAR_USER)
    description  = models.TextField(verbose_name=_("Description"), blank=True)
    thumbnail    = GenericRelation(MediaFile)
    date_expires = models.DateTimeField(verbose_name=_("Expiry Date"), null=True, blank=True)

    def can_have_api_key(self):
        """
        Check whether a given user is eligable for an API key, meaning it is either a
        Developer or Application user.
        """
        return self.user_type == self.DEVELOPER or self.user_type == self.APPLICATION

    def clean(self):
        """
        During form validation make sure that Developers and Applications cannot be saved
        without an e-mail adress. Otherwise we cannot send them their API Key.
        """
        if self.can_have_api_key() and not self.email:
            raise ValidationError(_("E-Mail address is required."))
    
    def reset_api_key(self, save_and_send_email: bool) -> str:
        """
        Presumed this is a Developer or Application User, calculate a new API key and change
        the user password accordingly. If the change is directly saved to database also an
        e-mail informing the human behind about the new API key. In any case the new key will
        be returned to the caller of the method.
        """
        # Sanity checks
        if not self.can_have_api_key():
            raise ValidationError(_("The user %s cannot have an API key.") % self.username)
    
        if not self.email:
            raise ValidationError(_("Cannot reset the API key of user %s without an e-mail address.") % self.username)

        # Reset key
        new_api_key = hash.generate_key(length=32, grouping=8)
        self.set_password(new_api_key)

        if save_and_send_email:
            self.save()

            text_template = template.loader.get_template("lernspiel_server/email/api_key_changed.txt")
            html_template = template.loader.get_template("lernspiel_server/email/api_key_changed.html")

            context = {
                "user_type":   self.get_user_type_display(),
                "username":    self.username,
                "first_name":  self.first_name,
                "new_api_key": new_api_key,

                # Note: Context processors are only executed when there is a HttpRequest
                "site":        site()["site"],
            }

            self.email_user(
                subject      = _("New API Key for %(user_type)s %(username)s") % context,
                message      = text_template.render(context),
                html_message = html_template.render(context),
            )

        return new_api_key

class UserGroup(Group):
    """
    Dummy class to move the Group model from `django.contrib.auth` into our own app.
    The users and groups stand together in the Admin.
    """
    class Meta():
        verbose_name        = _("User Group")
        verbose_name_plural = _("User Groups")
