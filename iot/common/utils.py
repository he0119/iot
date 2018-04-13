'''
Tools
'''
from datetime import timezone

def datetime2iso(datetime):
    '''datetime to ISO 8601 str'''
    if not datetime:
        return None
    #default timezone is utc
    if not datetime.tzinfo:
        datetime = datetime.replace(tzinfo=timezone.utc)
    return datetime.isoformat()
