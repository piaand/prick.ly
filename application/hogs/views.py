from application import app, db
from flask_login import login_required
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog
from application.hogs.forms import HogForm

@app.route("/hogs", methods=["GET"])
def hogs_index():
    return render_template("hogs/list.html", hogs = Hog.query.all())

@app.route("/hogs/new/")
@login_required
def hogs_form():
    return render_template("hogs/new.html", form = HogForm())

@app.route("/hogs/<hog_id>/", methods=["POST"])
@login_required
def hog_set_onduty(hog_id):

    hog = Hog.query.get(hog_id)
    hog.onduty = True
    db.session().commit()
  
    return redirect(url_for("hogs_index"))

@app.route("/hogs/", methods=["POST"])
@login_required
def hogs_create():
    form = HogForm(request.form)

    if not form.validate():
        return render_template("hogs/new.html", form = form)
    
    hog = Hog(form.name.data)
    hog.onduty = form.onduty.data
    db.session().add(hog)
    db.session().commit()

    return redirect(url_for("hogs_index"))
