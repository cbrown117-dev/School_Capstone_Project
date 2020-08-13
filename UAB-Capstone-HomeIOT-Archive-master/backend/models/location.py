# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from extensions.database import db


class Location(db.Model):
    __tablename__ = "location"
    locationId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    devices = db.relationship("Device", back_populates="location")

    def __repr__(self):
        return '<Location | Name: %r>' % self.name

    def __init__(self, name):
        self.name = name