# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.http import HttpResponse

def join_game(request, key):
    return HttpResponse("Join Game: %s" % key)

def edit_game(request, key):
    return HttpResponse("Edit Game: %s" % key)