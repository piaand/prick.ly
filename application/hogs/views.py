from application import app, db, login_required
from flask_login import current_user
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog
from application.hogs.forms import HogForm
from application.auth.models import User


@app.route("/hogs", methods=["GET"])
def hogs_index():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        user = User.query.get(user_id)
    else:
        user = User("Visitor","visitor","visit","GUEST")
    return render_template("hogs/list.html", hogs = Hog.find_popular_hogs(), user = user)

@app.route("/hogs/new/")
@login_required(role="ADMIN")
def hogs_form():
    return render_template("hogs/new.html", form = HogForm(), user = current_user)

@app.route("/hogs/<hog_id>/", methods=["POST"])
@login_required(role="ADMIN")
def hog_set_onduty(hog_id):

    hog = Hog.query.get(hog_id)
    hog.onduty = True
    db.session().commit()
  
    return redirect(url_for("hogs_index"))

@app.route("/hogs/<hog_id>/delete", methods=["POST"])
@login_required(role="ADMIN")
def hog_delete(hog_id):

    hog = Hog.query.get(hog_id)
    db.session.delete(hog)
    db.session().commit()
  
    return redirect(url_for("hogs_index"))

@app.route("/hogs/", methods=["POST"])
@login_required(role="ADMIN")
def hogs_create():
    form = HogForm(request.form)

    if not form.validate():
        return render_template("hogs/new.html", form = form)
    
    hog = Hog(form.name.data)
    hog.onduty = form.onduty.data
    db.session().add(hog)
    db.session().commit()

    return redirect(url_for("hogs_index"))
