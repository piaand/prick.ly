from application import db
from application.models import Base
from sqlalchemy.orm import relationship, backref

hog_identifier = db.Table('hog_identifier',
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.id')),
    db.Column('hog_id', db.Integer, db.ForeignKey('hog.id'))
)

class Reservation(Base):

    startTime = db.Column(db.DateTime, nullable=False)
    durationMin = db.Column(db.Integer, nullable=False)
    accountId = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    hogs = db.relationship("Hog", secondary=hog_identifier)

    def __init__(self, durationMin):
        self.startTime = db.func.current_timestamp()
        self.durationMin = durationMin
        self.verified = False
        
    def get_hogs(self):
        return self.hogs