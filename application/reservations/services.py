from application.reservations.forms import ReservationForm, SummaryForm, ReservationSelectForm
from flask import redirect, render_template, request, url_for

from application.hogs.models import Hog

import datetime
from datetime import timedelta

def get_available_hogs(request_time):
    
    if isinstance(request_time, datetime.datetime):
        start = request_time
    else: 
        start = datetime.datetime.strptime(request_time, '%Y-%m-%d')
    
    end = start + timedelta(days=1)
    hogs = Hog.find_available_hogs(start, end)
    print("Printing them hogs")
    print(hogs)
    hog_selection = []
    for hog in hogs:
        print("inside first loop")
        print(hog)
        choice = (hog['id'], hog['name'])
        hog_selection.append(choice)

    print("Printing them selection")
    print(hog_selection)
    
    return hog_selection