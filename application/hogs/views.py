from application import app, db
from flask import render_template, request
from application.hogs.models import Hog

@app.route("/hogs", methods=["GET"])
def hogs_index():
    return render_template("hogs/list.html", hogs = Hog.query.all())

@app.route("/hogs/new/")
def hogs_form():
    return render_template("hogs/new.html")

@app.route("/hogs/", methods=["POST"])
def hogs_create():
    hog = Hog(request.form.get("name"))

    db.session().add(hog)
    db.session().commit()
    return "hello world!"
