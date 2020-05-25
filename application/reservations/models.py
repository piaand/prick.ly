from application import db
from application.models import Base
from sqlalchemy.orm import relationship, backref

class Reservation(Base):

    startTime = db.Column(db.DateTime, nullable=False)
    durationMin = db.Column(db.Integer, nullable=False)
    accountId = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)

    def __init__(self, durationMin):
        self.startTime = db.func.current_timestamp()
        self.durationMin = durationMin
        self.verified = False
