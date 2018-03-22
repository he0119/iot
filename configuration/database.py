import os
import sys
from sqlalchemy import create_engine

from sqlalchemy import Column, String, create_engine, Boolean, Integer, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Old_DeviceData(Base):
    '''Device Data(id, time, temperature, relative_humidity, relay1_status, relay2_status)'''
    __tablename__ = 'device_data'
    __table_args__ = {'useexisting': True}
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, index=True)
    temperature = Column(String(32))
    relative_humidity = Column(String(32))
    relay1_status = Column(Boolean)
    relay2_status = Column(Boolean)

    def set_data(self, temperature, relative_humidity, relay1_status, relay2_status, time):
        self.time = time
        self.temperature = temperature
        self.relative_humidity = relative_humidity
        self.relay1_status = relay1_status
        self.relay2_status = relay2_status
        
    def __repr__(self):
        return '<DeviceData {}>'.format(self.time)

# 初始化数据库连接:
engine1 = create_engine('sqlite:///C:/Users/hmy01/Desktop/works/Working/iot/app12.db')
# 创建DBSession类型:
DBSession1 = sessionmaker(bind=engine1)
session1 = DBSession1()

class New_DeviceData(Base):
    '''Device Data(id, time, temperature, relative_humidity, relay1_status, relay2_status)'''
    __tablename__ = 'device_data'
    __table_args__ = {'useexisting': True}
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, index=True)
    temperature = Column(Float)
    relative_humidity = Column(Float)
    relay1_status = Column(Boolean)
    relay2_status = Column(Boolean)

    def set_data(self, temperature, relative_humidity, relay1_status, relay2_status, time):
        self.time = time
        self.temperature = temperature
        self.relative_humidity = relative_humidity
        self.relay1_status = relay1_status
        self.relay2_status = relay2_status
        
    def __repr__(self):
        return '<DeviceData {}>'.format(self.time)

# 初始化数据库连接:
engine2 = create_engine('sqlite:///C:/Users/hmy01/Desktop/works/Working/iot/app.db')
# 创建DBSession类型:
DBSession2 = sessionmaker(bind=engine2)
session2 = DBSession2()

u = session1.query(Old_DeviceData).all()
for i in u:
    a = New_DeviceData()
    a.set_data(None if i.temperature == 'Error' else float(i.temperature),
               None if i.relative_humidity == 'Error' else float(i.relative_humidity),
               i.relay1_status,
               i.relay2_status,
               i.time)
    session2.add(a)
    print(i.id)
session2.commit()