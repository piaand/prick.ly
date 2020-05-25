from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, validators
from wtforms.validators import NumberRange

class ReservationForm(FlaskForm):
    duration = IntegerField("How long session (in minutes)", validators=[NumberRange(min=5, max=60, message='one session should be between 5 and 60 minutes')])

    class Meta:
        csrf = False