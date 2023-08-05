from enum import Enum

__all__ = ["HTMLHeaderTags", "BytesConvertUnits"]


class HTMLHeaderTags(Enum):
    """Enum for HTML header tags"""

    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6


class BytesConvertUnits(Enum):
    """Enum for converting bytes to other units."""

    BYTE = BYTES = 1
    KB = 1e3
    MB = 1e6
    GB = 1e9
    TB = 1e12
    PB = 1e15
    EB = 1e18
    ZB = 1e21
    YB = 1e24
