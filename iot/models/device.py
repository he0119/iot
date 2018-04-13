'''
Device Model
'''
from datetime import datetime

from iot.common.db import db


class Device(db.Model):
    '''device model(id, name, schema)'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    schema = db.Column(db.PickleType)
    create_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_connect_on = db.Column(db.DateTime)
    offline_on = db.Column(db.DateTime)
    online_status = db.Column(db.Boolean)

    def change_status(self, status):
        '''Change online status'''
        self.online_status = status
        if status:
            self.last_connect_on = datetime.utcnow()
        else:
            self.offline_on = datetime.utcnow()

    def __repr__(self):
        return '<Device %r>' % self.name
