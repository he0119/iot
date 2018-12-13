"""Tools"""
from datetime import timezone
from enum import IntEnum, unique


def datetime2iso(datetime):
    """Datetime to ISO 8601 str."""
    if not datetime:
        return None
    # default timezone is utc
    if not datetime.tzinfo:
        datetime = datetime.replace(tzinfo=timezone.utc)
    return datetime.isoformat()

@unique
class DeviceDataType(IntEnum):
    integer = 1
    float = 2
    boolean = 3
    string = 4
