from flask import Flask
app = Flask(__name__)

# Use db hogs -- /// means hogs.db is at the same place as rest of the app
# Echo True means print out all queries
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hogs.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.hogs import models
from application.hogs import views

db.create_all()
