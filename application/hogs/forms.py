from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, validators

class HogForm(FlaskForm):
    name = StringField("Hedgehog's name", [validators.Length(min=3)])
    onduty = BooleanField("Put this hedgehog on duty")

    class Meta:
        csrf = False