# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import hashlib, uuid

def generate_key(length: int, grouping=0) -> str:
    """
    Generate a new key of the given length. By default the key will contains only hexadecimal
    characters without separators. If the grouping parameter is set to a positive number, minus
    signs will be inserted every N characters.

    This method uses the SHAKE128 algorithm, which can produce any number of characters.
    """
    hash_value = uuid.uuid4().bytes

    for i in range(72000):
        hash_value = hashlib.shake_128(hash_value).digest(length)

    result = hash_value.hex()

    if grouping > 0:
        result_parts = [result[i:i+grouping] for i in range(0, len(result), grouping)]
        result = '-'.join(result_parts)

    return result

def hash_key(key: str) -> str:
    """
    Calculate a hash value of the given key. The returned string includes the name
    and length of the used hash algorithm, in case we need distinguish multiple
    implementations in future.
    """
    hash_string = hashlib.shake_128(key.encode("utf-8")).hexdigest(32)
    return "shake_128:32:%s" % hash_string