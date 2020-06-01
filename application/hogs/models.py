from application import db
from application.models import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

class Hog(Base):

    name = db.Column(db.String(144), nullable=False)
    onduty = db.Column(db.Boolean, nullable=False)

    def __init__(self, name):
        self.name = name
        self.onduty = False
        
    @staticmethod
    def find_popular_hogs():
        stmt = text(" SELECT hog.name AS name, COALESCE(total, 0) FROM Hog"
                    " LEFT JOIN ("
                    " SELECT SUM(reservation.durationMin) AS total, hog_identifier.hog_id AS identify FROM reservation"
                    " LEFT JOIN hog_identifier ON hog_identifier.reservation_id = reservation.id"
                    " GROUP BY identify)"
                    " ON identify = hog.id"
                    " ORDER BY total DESC")
        res = db.engine.execute(stmt)
  
        for row in res:
            print(row[0])
            print(row[1])