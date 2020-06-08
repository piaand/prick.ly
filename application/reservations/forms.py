from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, BooleanField, IntegerField, validators
from wtforms.validators import NumberRange

class ReservationForm(FlaskForm):
    start = DateField('DatePicker', format='%Y-%m-%d')
    duration = IntegerField("How long session (in minutes)", validators=[NumberRange(min=5, max=60, message='one session should be between 5 and 60 minutes')])
    hog = StringField("Name of the hedgehog:", validators=[validators.Length(min=3)])

    class Meta:
        csrf = False
        
class SummaryForm(FlaskForm):
    hog = StringField("Write the name of the hedgehog:", validators=[validators.Length(min=3)])

    class Meta:
        csrf = False