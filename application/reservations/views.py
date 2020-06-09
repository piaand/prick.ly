from application import app, db
from flask_login import login_required, current_user
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog
from application.auth.models import User
from application.reservations.models import Reservation
from application.reservations.forms import ReservationForm, SummaryForm, ReservationSelectForm
from .services import get_available_hogs

import datetime
from datetime import timedelta

@app.route("/reservations", methods=["GET"])
@login_required
def reservations_index():
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    
    if user.is_admin():
        return render_template("reservations/list.html", reservations = Reservation.query.all(), user = user)
    else:
        return render_template("reservations/list.html", reservations = db.session.query(Reservation).filter(Reservation.account_id == user.get_id()), user = user)

@app.route("/reservations/new/")
@login_required
def reservations_form():
    
    form = ReservationForm()
    return render_template("reservations/new.html", form=form)

@app.route("/reservations/new/<start>/<duration>/")
@login_required
def reservations_form_select(start, duration):
    
    hogs = get_available_hogs(start)
    form = ReservationSelectForm()
    form.hog.choices = hogs   
    return render_template("reservations/new_select.html", form=form, start=start, duration=duration)

@app.route("/reservations/new/reservation", methods=["POST"])
@login_required
def reservation_update():

    form = ReservationForm(request.form)

    if not form.validate():
        return render_template("reservations/new.html", form = form)
    
    start = form.start.data
    duration = form.duration.data
    return redirect(url_for("reservations_form_select", start=start, duration=duration))

@app.route("/reservations/<reservation_id>/hog", methods=["POST"])
@login_required
def reservation_add_hedgehog(reservation_id):

    form = SummaryForm(request.form)
    
    hog = Hog.query.get(form.hog.data)
    book = Reservation.query.get(reservation_id)
    book.hogs.append(hog)

    db.session().commit()
    return redirect(url_for("reservation_hogs", reservation_id = reservation_id))

@app.route("/reservations/<reservation_id>/", methods=["POST"])
@login_required
def reservation_verification(reservation_id):
    
    book = Reservation.query.get(reservation_id)
    book.verified = True
    db.session().commit()
  
    return redirect(url_for("reservations_index"))

@app.route("/reservations/<reservation_id>/", methods=["GET"])
@login_required
def reservation_hogs(reservation_id):
    
    book = Reservation.query.get(reservation_id)
    required_time = book.start_time
    hogs = get_available_hogs(required_time)
    form = SummaryForm()
    form.hog.choices = hogs 
    return render_template("reservations/summary.html", hedgehogs = book.get_hogs(), booking = book, form = form)

@app.route("/reservations/<start>/<duration>/", methods=["POST"])
@login_required
def reservation_create(start, duration):
    
    form = ReservationSelectForm(request.form)
    format='%Y-%m-%d'
    hog = Hog.query.get(form.hog.data)
    start_dt = datetime.datetime.strptime(start, format)
    
    book = Reservation(duration, start_dt)
    book.account_id = current_user.id
    book.hogs.append(hog)

    db.session().add(book)
    db.session().commit()
    return redirect(url_for("reservations_index"))


@app.route("/reservations/<reservation_id>/delete", methods=["POST"])
@login_required
def reservation_delete(reservation_id):
    
    book = Reservation.query.get(reservation_id)
    db.session.delete(book)
    db.session().commit()
  
    return redirect(url_for("reservations_index"))
