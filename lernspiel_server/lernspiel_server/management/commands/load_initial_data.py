# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core                     import management
from django.core.management.base     import BaseCommand

class Command(BaseCommand):
    help = "Load fixtures will initial data for the Lernspiel Server"

    FIXTURES = [
        "lernspiel_server/site",
        "lernspiel_server/languages",
        "ls_game_definition/game_definitions",
        "ls_game_runtime/game_instances",
        "ls_ui_static_pages/header_main_menu",
        "ls_ui_static_pages/page_type_start_page",
    ]

    def handle(self, *args, **options):
        for fixture in self.FIXTURES:
            management.call_command("loaddata", fixture, verbosity=1)