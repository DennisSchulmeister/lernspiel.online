# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from . import views
from django.urls import path
from django.views.generic.base import RedirectView

app_name = "ls_ui_static_pages"

urlpatterns = [
    path("", RedirectView.as_view(url="/start")),

    # path("archive/", views.archive, {"blog_id": 3}),
    # path("about/", views.about, {"blog_id": 3}),
    # path("blog/<int:year>/", views.year_archive, {"foo": "bar"}),
    # path("<page_slug>-<page_id>/history/", views.history),
]