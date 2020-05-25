from application import app, db
from flask_login import login_required, current_user
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog
from application.reservations.models import Reservation
from application.reservations.forms import ReservationForm

@app.route("/reservations", methods=["GET"])
@login_required
def reservations_index():
    #this will eventually show only reservations by current_user.id
    return render_template("reservations/list.html", reservations = Reservation.query.all())

@app.route("/reservations/new/")
@login_required
def reservations_form():
    return render_template("reservations/new.html", form = ReservationForm())

@app.route("/reservations/<reservation_id>/", methods=["GET"])
@login_required
def reservation_hogs(reservation_id):
    
    book = Reservation.query.get(reservation_id)
    return render_template("reservations/summary.html", hedgehogs = book.get_hogs(), booking = book)

@app.route("/reservations/<reservation_id>/hog", methods=["POST"])
@login_required
def reservation_add_hedgehog(reservation_id):

	return redirect(url_for("reservations_index"))	

@app.route("/reservations/<reservation_id>/", methods=["POST"])
@login_required
def reservation_verification(reservation_id):

    book = Reservation.query.get(reservation_id)
    book.verified = True
    db.session().commit()
  
    return redirect(url_for("reservations_index"))

@app.route("/reservations/", methods=["POST"])
@login_required
def reservation_create():
    form = ReservationForm(request.form)

    if not form.validate():
        return render_template("reservations/new.html", form = form)
    
    hog_name = form.hog.data
    hog = Hog.query.filter_by(name=hog_name).first()
    
    if not hog:
        return render_template("reservations/new.html", form = form)
    
    book = Reservation(form.duration.data)
    book.accountId = current_user.id
    book.hogs.append(hog)

    db.session().add(book)
    db.session().commit()

    return redirect(url_for("reservations_index"))
