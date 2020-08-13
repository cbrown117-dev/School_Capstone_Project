# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from extensions.database import db
from sqlalchemy import DateTime


class EventLog(db.Model):
    __tablename__ = "eventlog"
    eventId = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer, db.ForeignKey("device.deviceId"))
    date = db.Column(DateTime, index=True, nullable=False)
    state = db.Column(db.Enum('OPENDOOR', 'CLOSEDOOR' ,'OPENWINDOW', 'CLOSEWINDOW','ON', 'OFF', 'OFFLINE', 'ERROR', 'INTTEMP', 'EXTTEMP', name="device_event_state"), default='OFF', index=True, nullable=False)
    temperature = db.Column(db.Integer)

    device = db.relationship("Device", back_populates="events")

    def __repr__(self):
        return f'<EventLog | DeviceId: {self.deviceId}>'

    def __init__(self, device, state, date, temperature):
        self.device = device
        self.state = state
        self.date = date
        self.temperature = temperature