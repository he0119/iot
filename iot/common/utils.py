'''
Tools
'''
from datetime import timezone
from enum import IntEnum, unique


def datetime2iso(datetime):
    '''datetime to ISO 8601 str'''
    if not datetime:
        return None
    # default timezone is utc
    if not datetime.tzinfo:
        datetime = datetime.replace(tzinfo=timezone.utc)
    return datetime.isoformat()

@unique
class DataType(IntEnum):
    integer = 0
    float = 1
    string = 2
    boolean = 3
