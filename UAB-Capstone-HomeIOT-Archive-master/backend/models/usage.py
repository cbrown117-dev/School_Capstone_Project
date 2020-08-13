# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from extensions.database import db
from datetime import datetime
from sqlalchemy import DateTime


class Usage(db.Model):
    __tablename__ = "usage"
    usageId = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer, db.ForeignKey("device.deviceId"))
    date = db.Column(DateTime, nullable=False)
    type = db.Column(db.Enum('water', 'electric', name="utility_type"), nullable=False)
    data = db.Column(db.Float)

    device = db.relationship("Device", back_populates="usages")

    def __repr__(self):
        return f'<Usage | Type: {self.type} | Date: {self.date}>'

    def __init__(self, device: 'Device', date: datetime, type: str, data: int):
        self.device = device
        self.date = date
        self.type = type
        self.data = data