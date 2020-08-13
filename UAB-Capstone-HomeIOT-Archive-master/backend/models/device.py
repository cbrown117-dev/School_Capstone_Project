# TODO: Create device model
# deviceId: int, pk, ai
# locationId: int, fk to location: locationId
# name: varchar
# type: enum
# enum of types:
# - door, no params
# - window, no params
# - water, p1: current Gallons Per Minute (GPM)
# - light, p1: Wattage
# - hvac, p1: low_f, p2: high_f, p3: ext_f, p4: int_f

# state: enum(ON, OFF, OFFLINE, ERROR)


# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from extensions.database import db
from sqlalchemy import DateTime


class Device(db.Model):
    __tablename__ = "device"
    deviceId = db.Column(db.Integer, primary_key=True)
    locationId = db.Column(db.Integer, db.ForeignKey("location.locationId"))
    name = db.Column(db.String(255), unique=True, nullable=False)
    type = db.Column(db.Enum('door', 'window', 'water', 'electric', 'light', 'hvac', name="device_type"), nullable=False)
    state = db.Column(db.Enum('ON', 'OFF', 'OFFLINE', 'ERROR', name="device_state"), default='OFF', nullable=False)
    lastUpdated = db.Column(DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    location = db.relationship("Location", back_populates="devices")
    events = db.relationship("EventLog", back_populates="device")
    usages = db.relationship("Usage", back_populates="device")

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __init__(self, location, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.location = location


class Door(Device):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'door'
    }


class Window(Device):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'window'
    }


class Water(Device):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'water'
    }
    # Gallons Per Minute for water flow
    gpm = db.Column(db.INTEGER, default=0)


class Electric(Device):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'electric'
    }
    wattage = db.Column(db.INTEGER)
    
    def __init__(self, location, x, y, name, wattage):
        self.x = x
        self.y = y
        self.name = name
        self.wattage = wattage
        self.location = location

    def __repr__(self):
        return f'<Device({self.__class__.__name__}) | Name: {self.name}, Wattage: {self.wattage}>'


class Light(Electric):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'light'
    }


class HVAC(Electric):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'hvac'
    }
    set_f = db.Column(db.INTEGER, default=0)
    high_f = db.Column(db.INTEGER, default=0)
    low_f = db.Column(db.INTEGER, default=0)
    ext_f = db.Column(db.INTEGER, default=0)
    int_f = db.Column(db.INTEGER, default=0)

    def __repr__(self):
        return f'<Device({self.__class__.__name__})  ' \
               f'| Name: {self.name}, ' \
               f'High({self.high_f}) ' \
               f'Low({self.low_f}) ' \
               f'Ext({self.ext_f}) ' \
               f'Int({self.int_f})>'

