# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

GAME_TYPES = {}

def register_game_type(game_type: str, label: str):
    """
    Register a new game type that can be chosen for new games. Usually this function
    should be called in the `ready()` method of the `AppConfig` class of each Django
    application that implements game types.

    Care must be taken to obey the rule from Django, that imports are only allowed,
    once an application becomes ready. A typical `AppConfig` class therefor looks
    like this:

    ```python
    class MyAppConfig(AppConfig):
        name         = "ls_games_example"
        verbose_name = _("Games: Example")

        def ready(self):
            from ls_games_core.utils.game_types import register_game_type
            register_game_type("EXAMPLE", _("Example"))
    ```
    """
    GAME_TYPES[game_type] = label