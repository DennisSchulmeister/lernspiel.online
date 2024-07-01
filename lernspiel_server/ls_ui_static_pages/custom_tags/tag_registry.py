# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

tag_names = []
tag_definitions = {}

def register(name, example="", help="", func=None):
    """
    Decorator to register a new custom tag. Use it like so:

    ```python
    from .custom_tags import tag_registry

    @tag_registry.register(
        name="my-tag",
        example="{my-tag xyz}",
        help=_("...")
    )
    def my_tag_handler(tagname: str, xyz: str) -> str:
        pass
    ```

    The handler function will receive the name of the matched custom tag as well as
    positional arguments for the tag parameters.
    """
    def inner_decorator(func1):
        global tag_definitions, tag_names

        tag_definitions[name] = {
            "example": example,
            "help":    help,
            "func":    func1
        }

        tag_names = list(tag_definitions.keys())
        tag_names.sort()

        return func1

    if func:
        return inner_decorator(func)
    else:
        return inner_decorator
