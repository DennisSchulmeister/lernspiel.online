# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

def calc_file_path(object, filename):
    """
    Callable for the `upload_to` property of `model.FileField`. Determines the upload bath
    by joining the app label and model name.

    The first parameter normally is the model's `_meta` attribute. But `self.content_type`,
    if it is a `models.ForeignKey` from a generic relation, can make sense to use the app
    name and label of the foreign model, instead.
    """
    model = object.model if type(object) is str else object.model.__name__

    return "%(app_label)s/%(model)s/%(filename)s" % {
        "app_label": object.app_label,
        "model":     model,
        "filename":  filename,
    }