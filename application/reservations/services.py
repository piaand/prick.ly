from application.reservations.forms import ReservationForm, SummaryForm, ReservationSelectForm
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog
from application.reservations.models import Reservation

import datetime
from datetime import timedelta

def validate_start_time(time):
    if time >= datetime.datetime.today():
        return True
    else:
        return False

def create_start_time(time):
    if isinstance(time, datetime.datetime):
        start = time
    else: 
        start = datetime.datetime.strptime(time, '%Y-%m-%d')
    
    return start  

def get_available_hogs(request_time):
    
    start = create_start_time(request_time)
    end = start + timedelta(days=1)
    hogs = Hog.find_available_hogs(start, end)
    hog_selection = []
    for hog in hogs:
        choice = (hog['id'], hog['name'])
        hog_selection.append(choice)
    
    return hog_selection

def create_booking(duration, start, id, hog):
    start_dt = create_start_time(start)
    book = Reservation(duration, start_dt)
    book.account_id = id
    book.hogs.append(hog)
    return book