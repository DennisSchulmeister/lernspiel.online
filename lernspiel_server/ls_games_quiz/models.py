# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.utils.translation import gettext_lazy as _

from lernspiel_server.db import AbstractModel

# TODO: Quiz games with 1:n categories with 1:n questions with 1:n answers
# Question settings:
#  - Type of question
#  - Shuffle answers
#  - Number of selectable answers
# Answer settings:
#  - Text
#  - Description (for assignment questions)
#  - Wrong/correct/partially correct