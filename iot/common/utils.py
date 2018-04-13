'''
Tools
'''
from datetime import timezone

def datetime2iso(datetime):
    '''datetime to ISO 8601 str'''
    if not datetime:
        return None
    datetime = datetime.replace(tzinfo=timezone.utc)
    return datetime.isoformat()
