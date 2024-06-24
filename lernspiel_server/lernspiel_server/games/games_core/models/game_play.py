# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.utils.translation import gettext_lazy as _

from ....core_platform.db import AbstractModel, CreatedModifiedByMixin

class GameSession(AbstractModel, CreatedModifiedByMixin):
    """
    xxx
    """
    # content type for inheritance

    join_key = models.CharField(verbose_name=_("Join Key"), max_length=64, editable=False)

    def __init__(self):
        self.reset_join_key()
    
    def reset_join_key(self, save: bool = False) -> str:
        """
        Calculate new join key and temporarily put it to `self.new_join_key` before
        returning it. Also change `join_key` to the new hashed value.
        """
        self.new_join_key = hash.generate_key(10)
        self.join_key.default = hash.hash_key(self.new_join_key)

        if save:
            self.save()
        
        return self.new_join_key


class Team(AbstractModel):
    """
    xxx
    """
    pass

class Player(AbstractModel):
    """
    xxx
    """
    pass
    # emoji

class ChatMessage(AbstractModel):
    """
    xxx
    """
    pass