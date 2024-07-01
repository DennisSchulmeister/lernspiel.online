# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import re, threading
from django.conf   import settings
from .tag_registry import tag_definitions

class NestingOverflowError(Exception):
    """
    Possible infinite loop was detected while resolving tag contents. This usually
    occurs because a snippet directly or indirectly references itself. Will be
    silently ignored in production.
    """
    pass

class UnknownTagError(Exception):
    """
    Unknown tag name. Lets the application crash when debug mode is on and will be
    silently ignored in production.
    """
    pass

context_stack = threading.local()
context_stack.value = []

nesting_level = threading.local()
nesting_level.value = 0

# Super fancy regex to split a text into `(text, tag, text, tag, …)` tokens.
# Curly braces will be stripped from the tags, leaving just their contents in tact.
TAG_REGEX = re.compile(r"(?<!\\)\{(.*?)\}")

# Maximum allowed nesting level
MAX_NESTING_LEVEL = 20

def replace_tags(text: str, context: dict) -> str:
    """
    Returns the given string with all `{tags}` replaced.

    Tags can have any number of parameters which are just splitted by spaces.
    If a parameters contains spaces itself it must be surrounded by single
    quotes or double quotes. Examples:

        {assets}
        {mailto test@example.com}
        {snippet "fine print"}
        {tag foo bar baz}

    In debug mode, unknown tags raise an `UnknownTagError`. If more then 20 levels
    of recursion are detected (snippets including snippets, …) an `NestingOverflowError`
    will be raised. Both errors will be silently ignored in production.
    """
    nesting_level.value += 1
    context_stack.value.append(context)

    if nesting_level.value >= MAX_NESTING_LEVEL:
        if settings.DEBUG:
            raise NestingOverflowError("Maximum allowed nesting of custom tags exceeded.")
        else:
            return text
    
    tokens = TAG_REGEX.split(text)
    is_tag = True
    result = ""

    for token in tokens:
        is_tag = not is_tag

        if not is_tag:
            result += token
        else:
            result += _apply_tag("{%s}" % token, _parse_tag(token))

    nesting_level.value -= 1
    context_stack.value.pop()

    return result

def _parse_tag(token):
    """
    Given a custom tag stripped from the curly braces, e.g.`my-tag arg1 "arg 2"`, parse the
    string and return a list with the tag name followed by its arguments. Arguments in quotes
    will be treated as a single value.
    """
    parsed  = []
    quote   = ""
    arg_val = ""
    arg_end = False

    for char in token:
        if char == '"' or char == "'":
            if not quote:
                quote = char
            else:
                arg_end = True

        if char == " " and not quote:
            arg_end = True

        if arg_end:
            parsed.append(arg_val)

            arg_end = False
            arg_val = ""
            quote   = ""
        elif not char == quote:
            arg_val += char

    if arg_val:
        parsed.append(arg_val)

    return parsed

def _apply_tag(unparsed: str, parsed: list[str]) -> str:
    """
    Apply a tag after it has been successfully parsed. Takes the original string
    and the result of `_parse_tag()` and returns its replacement text.
    """
    if not parsed:
        return unparsed

    try:
        func = tag_definitions[parsed[0]]["func"]
        return func(parsed[0], parsed[1:])
    except KeyError:
        if settings.DEBUG:
            raise UnknownTagError("Unknown custom tag: %s" % parsed[0])
        else:
            return unparsed
