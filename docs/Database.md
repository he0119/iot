# Database
## User
```python
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(64), index=True, unique=True, nullable=False)
email = db.Column(db.String(120), index=True, unique=True, nullable=False)
password_hash = db.Column(db.String(128), nullable=False)
devices = db.relationship('Device', backref='user', lazy='dynamic')
```
## Device
```python
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(64), nullable=False, unique=True)
schema = db.Column(db.PickleType, nullable=False)
display = db.Column(db.PickleType, nullable=False)
create_on = db.Column(db.DateTime, default=datetime.utcnow())
last_connect_on = db.Column(db.DateTime)
offline_on = db.Column(db.DateTime)
online_status = db.Column(db.Boolean)
user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
data = db.relationship('DeviceData', backref='device', lazy='dynamic')
```
## DeviceData
```python
id = db.Column(db.Integer, primary_key=True)
time = db.Column(db.DateTime, index=True)
data = db.Column(db.String(120))
device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
```
