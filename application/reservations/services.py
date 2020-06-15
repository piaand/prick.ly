from application.reservations.forms import ReservationForm, SummaryForm, ReservationSelectForm
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog
from application.reservations.models import Reservation

import datetime
from datetime import timedelta

def get_available_hogs(request_time):
    
    if isinstance(request_time, datetime.datetime):
        start = request_time
    else: 
        start = datetime.datetime.strptime(request_time, '%Y-%m-%d')
    
    end = start + timedelta(days=1)
    hogs = Hog.find_available_hogs(start, end)
    hog_selection = []
    for hog in hogs:
        choice = (hog['id'], hog['name'])
        hog_selection.append(choice)
    
    return hog_selection

def create_booking(duration, start, id, hog):
    format='%Y-%m-%d'
    start_dt = datetime.datetime.strptime(start, format)
    
    book = Reservation(duration, start_dt)
    book.account_id = id
    book.hogs.append(hog)
    return book