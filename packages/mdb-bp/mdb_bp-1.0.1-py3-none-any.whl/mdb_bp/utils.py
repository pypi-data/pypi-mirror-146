import hashlib
import os
from datetime import datetime

from mdb_bp.const import CONST_SALT_BYTE_LENGTH


def build_table(table):
    col_widths = [0] * len(table)

    for y in range(len(table)):
        for x in table[y]:
            if col_widths[y] < len(x):
                col_widths[y] = len(x)

    resp = ""
    for x in range(len(table[0])):
        for y in range(len(table)):
            resp += table[y][x].ljust(col_widths[y]) + ' '
        resp += "\n"
    return resp


def random_bytes(length):
    rand_bytes = os.urandom(length)
    return rand_bytes


def bytes_to_string(byte_array):
    resp = "[{}".format(byte_array[0])
    for index in range(1, len(byte_array)):
        resp += " {}".format(byte_array[index])
    resp += "]"
    return resp


def interpolate_params(query, params):
    # Check for valid inputs
    assert query.count("?") == len(params), \
        "the query received {} parameters, but received {}".format(query.count("?"), len(params))

    # Initialize basic variables
    params_pos = 0
    resp = ""

    # Loop through the characters in the string and fill in the parameters in params
    for char in query:
        if char == '?':
            # Grab the param
            param = params[params_pos]

            # Switch on the type of the input parameter
            if param is None:
                resp += "NULL"
            elif type(param) is datetime:
                # Grab the location from the cfg and format accordingly
                # datetime.
                raise Exception("datetime not supported")
            # elif data_type == "json":
            #     raise Exception("json not supported")
            elif type(param) is str:
                if '"' in param: param = param.replace('"', '""')
                resp += "\"{}\"".format(param)
            elif type(param) is bytes or type(param) is bytearray:
                if len(param) == 0:
                    resp += "[]"
                else:
                    resp += "[{}".format(param[0])
                    for index in range(1, len(param)):
                        resp += " {}".format(param[index])
                    resp += "]"
            else:
                resp += "{}".format(param)

            # Increment the pos
            params_pos += 1
        else:
            # Add current char to the response
            resp += char

    return resp


def hash_password(password):
    """Hash a password for storing."""

    # The salt is used to prevent the use of a hash table lookup attack
    # The salt should never be less than 32 bytes
    salt = random_bytes(CONST_SALT_BYTE_LENGTH)

    # A MAC with 32 bytes of output has 256-bit security strength -- if you use at least a 32-byte-long key.
    d = hashlib.sha3_256()

    # Write the salt to the hash
    d.update(salt)

    # Write the password to the hash
    # TODO: Update encoding to reference the config
    d.update(password.encode('utf-8'))

    # Read the output of the hash
    pw_hash = d.digest()

    return salt, pw_hash