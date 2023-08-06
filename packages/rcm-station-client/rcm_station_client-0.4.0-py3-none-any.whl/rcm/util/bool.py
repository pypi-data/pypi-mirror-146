#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
Util methods for booleans
"""


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.

    This replaces the deprecated distutils.util strtobool from python 3.10.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    raise ValueError(f'invalid truth value {val}')
