from application import db
from application.models import Base


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    access = db.Column(db.String(144), nullable=False)
    reservations = db.relationship("Reservation", backref='account', lazy=True)

    def __init__(self, name, username, password, access):
        self.name = name
        self.username = username
        self.password = password
        self.access = access
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def is_admin(self):
        if self.access == "ADMIN":
            return True
    
    def roles(self):
        return self.access