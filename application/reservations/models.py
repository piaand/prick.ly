from application import db
from application.models import Base
from sqlalchemy.orm import relationship, backref

class Reservation(Base):

    startTime = db.Column(db.DateTime)
    durationMin = db.Column(db.Integer)
    userId = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, startTime):
        self.startTime = startTime
        self.durationMin = 30
