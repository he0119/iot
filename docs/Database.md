# Database

## User

```python
__tablename__ = 'user'
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(64), index=True, unique=True, nullable=False)
email = db.Column(db.String(120), index=True, unique=True, nullable=False)
password_hash = db.Column(db.String(128), nullable=False)
devices = db.relationship('Device', backref='user', lazy='dynamic')
```

## Device

```python
__tablename__ = 'device'
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(64), nullable=False, unique=True)
display_name = db.Column(db.String(64))
create_on = db.Column(db.DateTime, default=datetime.utcnow())
last_connect_on = db.Column(db.DateTime)
offline_on = db.Column(db.DateTime)
online_status = db.Column(db.Boolean)
data = db.relationship("DeviceData", backref='device', lazy='dynamic')
schema = db.relationship("DeviceSchema", backref='device', lazy='dynamic')
user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

## DeviceData

```python
__tablename__ = 'devicedata'
id = db.Column(db.Integer, primary_key=True)
time = db.Column(db.DateTime, index=True, nullable=False)
data = db.Column(db.JSON, nullable=False)
device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
```

## DeviceSchema

```python
__tablename__ = 'deviceschema'
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(64), nullable=False, unique=True)
display_name = db.Column(db.String(64))
data_type = db.Column(db.Integer, nullable=False)
show = db.Column(db.Boolean, nullable=False)
allow_control = db.Column(db.Boolean, nullable=False)
device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
```
