# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import hashlib, uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from ...db import AbstractModel, EditKeyMixin
from ...models import MediaFile

class Quiz(AbstractModel, EditKeyMixin):
    """
    A single quiz with questions and answers.
    """
    name = models.CharField(verbose_name=_("Quiz Name"), max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # TODO
        return ""
    
class Question(AbstractModel):
    """
    A single quiz question.
    """
    SINGLE_CHOICE   = 1
    MULTIPLE_CHOICE = 2
    GAP_TEXT        = 3
    SORT_ANSWERS    = 4
    ASSIGN_ANSWERS  = 5

    _QUESTION_TYPES = (
        (SINGLE_CHOICE,   _("Single Choice")),
        (MULTIPLE_CHOICE, _("Multiple Choice")),
        (GAP_TEXT,        _("Gap Text")),
        (SORT_ANSWERS,    _("Sort Answers")),
        (ASSIGN_ANSWERS,  _("Assign Answers")),
    )

    quiz    = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text    = models.CharField(verbose_name=_("Question Text"), max_length=255)
    detail  = models.TextField(verbose_name=_("Detail Text"), blank=True)
    media   = GenericRelation(MediaFile)
    type    = models.SmallIntegerField(verbose_name=_("Question Type"), choices=_QUESTION_TYPES)
    shuffle = models.BooleanField(verbose_name=_("Shuffle Answers"))

    class Meta:
        ordering = ["text"]
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

        indexes = [
            models.Index(fields=["text"])
        ]
    
    def __str__(self):
        return self.text

    def get_absolute_url(self):
        # TODO
        return ""

class Answer(AbstractModel):
    """
    Possible answer to a question.
    """
    WRONG   = 1
    PARTIAL = 2
    CORRECT = 3

    _ANSWER_TYPES = (
        (WRONG,   _("Wrong Answer")),
        (PARTIAL, _("Partially Correct Answer")),
        (CORRECT, _("Correct Answer")),
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number   = models.SmallIntegerField(verbose_name=_("Number"))
    type     = models.SmallIntegerField(verbose_name=_("Answer Type"), choices=_ANSWER_TYPES)
    text     = models.CharField(verbose_name=_("Answer Text"), max_length=255)
    assign   = models.CharField(verbose_name=_("Correct Assignment"), max_length=255, blank=True)

    class Meta:
        ordering = ["number", "text"]
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

        indexes = [
            models.Index(fields=["question", "number"]),
        ]
    
    def __str__(self):
        return self.text