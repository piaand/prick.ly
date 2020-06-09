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
        stmt = text(" SELECT hog.name AS name, COALESCE(mins, 0) AS total, hog.onduty AS onduty, hog.id AS id FROM hog"
                    " LEFT JOIN ("
                    " SELECT SUM(reservation.duration_min) AS mins, hog_identifier.hog_id AS identify FROM reservation"
                    " LEFT JOIN hog_identifier ON hog_identifier.reservation_id = reservation.id"
                    " GROUP BY identify) AS derivedtable"
                    " ON identify = id"
                    " ORDER BY total DESC")
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"name":row[0], "minutes":row[1], "onduty":row[2], "id":row[3]})
        
        return response
    
    @staticmethod
    def find_available_hogs(start, end):
        stmt = text(" SELECT hog.name AS name, hog.id AS id FROM hog"
                    " WHERE id NOT IN"
                    " (SELECT hog.id AS id_booked FROM hog"
                    " LEFT JOIN ("
                    " SELECT hog_identifier.hog_id AS identify, reservation.start_time AS start_time FROM reservation"
                    " LEFT JOIN hog_identifier ON hog_identifier.reservation_id = reservation.id) AS derivedtable"
                    " ON identify = hog.id"
                    " WHERE NOT (start_time < :start OR start_time > :end))"
                    " AND (hog.onduty = True)").params(start=start, end=end)
                    
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        
        return response