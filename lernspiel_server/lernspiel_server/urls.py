# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf                     import settings
from django.conf.urls.static         import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls                     import include, path
from django.views.generic.base       import RedirectView
from ninja                           import NinjaAPI

from ls_game_meta.api                import router as game_meta_api_router
from ls_game_definition.api          import router as game_definition_api_router
from ls_game_runtime.api             import router as game_runtime_api_router

from .admin                          import admin_site
from .                               import views

api = NinjaAPI()
api.add_router("/meta/",       game_meta_api_router)
api.add_router("/definition/", game_definition_api_router)
api.add_router("/runtime/",    game_runtime_api_router)

urlpatterns = [
    # path("", RedirectView.as_view(url="/pages")),
    # TODO: Prototype - Remove again
    path("", RedirectView.as_view(url="/play")),

    path("create/", include("ls_ui_game_creator.urls")),
    path("play/",   include("ls_ui_game_player.urls")),
    path("pages/",  include("ls_ui_static_pages.urls")),
    path("api/",    api.urls),
    path("admin/",  admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path("error/400", views.Error400.as_view()),
        path("error/403", views.Error403.as_view()),
        path("error/404", views.Error404.as_view()),
        path("error/500", views.Error500.as_view()),
    ]
