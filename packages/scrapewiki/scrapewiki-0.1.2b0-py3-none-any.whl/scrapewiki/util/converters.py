from ..structures import BytesConvertUnits

__all__ = ["convert_bytes_to"]


def convert_bytes_to(unit: BytesConvertUnits | int, bytes: int) -> int:
    """Convert bytes to other units."""
    if isinstance(unit, int):
        return bytes // unit
    elif isinstance(unit, BytesConvertUnits):
        return bytes // unit.value
    else:
        raise TypeError(f"unit must be an int or a BytesConvertUnits, not {type(unit)}")
