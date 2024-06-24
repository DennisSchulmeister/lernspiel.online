# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import hashlib, uuid

def generate_key(length: int) -> str:
    """
    Generate a new key of the given length. The key will contains only hexadecimal
    characters without separators. Internally a UUID is hashed with SHAKE128, which
    can produce any number of characters.
    """
    return hashlib.shake_128(uuid.uuid().bytes).hexdigest(length)

def hash_key(key: str) -> str:
    """
    Calculate final hash value of the given key. Can be used to update the key in
    the database or to compare received key with the saved one.
    """
    return "shake_128:%s:%s" % (len(str) / 2, hashlib.shake_128(key).hexdigest(32))
