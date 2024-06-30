# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

import lernspiel_server.utils.models as db_utils
from .shared import MediaFile, SourceFile


class Category(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    Hierarchical categories for game components. These define a directory-like
    structure to cluster related components and make them easier to find in
    the game editor UI.
    """
    name       = models.CharField(verbose_name=_("Name"), max_length=255)
    parent     = models.ForeignKey("self", verbose_name=_("Parent Category"), on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.SmallIntegerField(verbose_name=_("Sort Order"))

    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)
    
    class Meta:
        verbose_name        = _("Meta: Category")
        verbose_name_plural = _("Meta: Categories")
        ordering            = ["sort_order"]      # "parent" -> Infinite loop caused by ordering.
        
        indexes = [
            models.Index(fields=["parent", "sort_order"]),
            models.Index(fields=["parent", "name"]),
        ]

    def __str__(self):
        return self.name

# TODO: Mixin class for translations to reduce code duplication
class Category_T(db_utils.UUIDMixin):
    parent   = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="translations")
    language = db_utils.LanguageField()
    label    = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label


class GameComponentMeta(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    Meta description of a game component, the main building block for games.
    """
    # General information
    def _calc_file_path(self, filename):
        return db_utils.calc_file_path(self._meta, filename)
    
    name       = models.CharField(verbose_name=_("Name"), max_length=255, unique=True)
    category   = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail  = models.FileField(verbose_name=_("Thumbnail"), upload_to=_calc_file_path, null=True, blank=True)

    # Translated texts
    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)

    # Source files
    media_files  = GenericRelation(MediaFile)
    source_files = GenericRelation(SourceFile)

    # Django meta information
    class Meta:
        verbose_name        = _("Meta: Game Component")
        verbose_name_plural = _("Meta: Game Components")
        ordering            = ["category", "name"]
        indexes             = [models.Index(fields=["name"])]
    
    def __str__(self):
        return self.name

class GameComponentMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]

    def __str__(self):
        return self.label


class TypedValueMixin(models.Model):
    """
    Mixin for properties and parameters which define typed data values.
    """
    PLAIN_TEXT     = "plain"
    FORMATTED_TEXT = "text"
    NUMBER         = "num"
    BOOL           = "bool"
    DICTIONARY     = "dict"

    _DATA_TYPES = {
        PLAIN_TEXT:     _("Plain Text"),
        FORMATTED_TEXT: _("Formatted Text"),
        NUMBER:         _("Number"),
        BOOL:           _("Boolean"),
        DICTIONARY:     _("Dictionary"),
    }

    name      = models.CharField(verbose_name=_("Name"), max_length=100)
    data_type = models.CharField(verbose_name=_(""), max_length=10, choices=_DATA_TYPES)
    length    = models.PositiveSmallIntegerField(verbose_name=_("Length"), null=True, blank=True)
    is_array  = models.BooleanField(verbose_name=_("Is Array"))

    class Meta:
        abstract = True


class PropertyMeta(db_utils.UUIDMixin, TypedValueMixin):
    """
    Named property of a game component. Properties define the state data of a game event.
    They can either be set statically when a game is built or dynamically at runtime through
    the game logic scripts.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="properties")
    
    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Meta: Property")
        verbose_name_plural = _("Meta: Properties")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class PropertyMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(PropertyMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label


class EventMeta(db_utils.UUIDMixin):
    """
    Named event of a game component. Game components emit events to trigger game logic, e.g.
    when a button is pressed or a timeout expires. Game logic scripts can subscribe to these
    events to update the game state by setting property values of the game components.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="events")
    name   = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Meta: Event")
        verbose_name_plural = _("Meta: Events")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class EventMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(EventMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label


class EventParameterMeta(db_utils.UUIDMixin, TypedValueMixin):
    """
    Named event parameter of an event. These are parameters that are passed to event subscribers.
    They share the same semantics than game component properties but are temporary and only bound
    to a single event occurrence.
    """
    parent = models.ForeignKey(EventMeta, on_delete=models.CASCADE, related_name="parameters")

    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Meta: Parameter")
        verbose_name_plural = _("Meta: Parameters")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class EventParameterMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(EventParameterMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label


class SlotMeta(db_utils.UUIDMixin):
    """
    Named slot of a game component. Slots define the areas, where a component can embed
    child components. This is very similar to web components that can also have multiple
    named slots where child elements can be inserted.
    """
    parent = models.ForeignKey(GameComponentMeta, on_delete=models.CASCADE, related_name="slots")
    name   = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    def get_translations(self, language: str = "") -> QuerySet:
        return db_utils.get_translations(self, language)
    
    class Meta:
        verbose_name        = _("Meta: Slot")
        verbose_name_plural = _("Meta: Slots")
        ordering            = ["parent", "name"]
        indexes             = [models.Index(fields=["parent", "name"])]
    
    def __str__(self):
        return self.name

class SlotMeta_T(db_utils.UUIDMixin):
    parent      = models.ForeignKey(SlotMeta, on_delete=models.CASCADE, related_name="translations")
    language    = db_utils.LanguageField()
    label       = models.CharField(verbose_name=_("Label"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]
    
    def __str__(self):
        return self.label
