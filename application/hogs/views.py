from application import app, db
from flask import redirect, render_template, request, url_for
from application.hogs.models import Hog

@app.route("/hogs", methods=["GET"])
def hogs_index():
    return render_template("hogs/list.html", hogs = Hog.query.all())

@app.route("/hogs/new/")
def hogs_form():
    return render_template("hogs/new.html")

@app.route("/hogs/<hog_id>/", methods=["POST"])
def hog_set_onduty(hog_id):

    hog = Hog.query.get(hog_id)
    hog.onduty = True
    db.session().commit()
  
    return redirect(url_for("hogs_index"))

@app.route("/hogs/", methods=["POST"])
def hogs_create():
    hog = Hog(request.form.get("name"))

    db.session().add(hog)
    db.session().commit()
    return redirect(url_for("hogs_index"))
