from application import db
from application.models import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import text

hog_identifier = db.Table('hog_identifier',
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.id')),
    db.Column('hog_id', db.Integer, db.ForeignKey('hog.id'))
)

class Reservation(Base):

    start_time = db.Column(db.DateTime, nullable=False)
    duration_min = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    hogs = db.relationship("Hog", secondary=hog_identifier)

    def __init__(self, duration_min):
        self.start_time = db.func.current_timestamp()
        self.duration_min = duration_min
        self.verified = False
        
    def get_hogs(self):
        return self.hogs