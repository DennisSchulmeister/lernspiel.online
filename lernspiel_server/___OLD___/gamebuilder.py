# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from ..db import UUIDMixin, EditKeyMixin
from ..models import MediaFile
from ..quizzes.models import Question
from ..gamedev.models import GameType

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

class GameDefinition(models.Model, UUIDMixin, EditKeyMixin):
    """
    Header data for a game definition.
    """
    name  = models.CharField(verbose_name=_("Name"), max_length=255)
    type  = models.ForeignKey(GameType, verbose_name=_("Game Type"), on_delete=models.CASCADE)
    media = GenericRelation(MediaFile)

    description = models.TextField(verbose_name=_("Description"), blank=True)
    last_access = models.DateTimeField(verbose_name=_("Last Access"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
    
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["last_access", "id"])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # TODO
        return ""
    
class AbstractGameElement(models.Model, UUIDMixin):
    """
    Abstract base class for game elements. Game elements can be questions, text panels
    and possibly many things more in future.
    """
    pass
    # name
    # state = START, RUNNING, END
    # order
    # background (CSS?)

class QuestionElement(AbstractGameElement):
    """
    A quiz question within a game. This links a `Question` model object from the quizzes
    app to a game.
    """
    question = models.ForeignKey(Question, on_delete=models.SET_DEFAULT, default="", blank=True)

class AnswerScoringRule(models.Model, UUIDMixin):
    """
    An answer to a quiz question within a game. Of course the answers are already linked
    to the questions inside the quizzes app. But here additional information on how to
    score each answer and control the game flow is added.
    """
    # points
    # wrong points for assignment questions
    # goto game element (by name), otherwise next

class TextPanelElement(AbstractGameElement):
    """
    A simple non-interactive game element that simply shows some textual information
    before the game continues.
    """
    text = models.TextField(verbose_name=_("Text"))
