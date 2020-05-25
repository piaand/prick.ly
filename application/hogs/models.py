from application import db
from application.models import Base
from sqlalchemy.orm import relationship

class Hog(Base):

    name = db.Column(db.String(144), nullable=False)
    onduty = db.Column(db.Boolean, nullable=False)

    def __init__(self, name):
        self.name = name
        self.onduty = False
