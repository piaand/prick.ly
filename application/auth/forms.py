from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class SignupForm(FlaskForm):
    name = StringField("Your full name", [validators.Length(min=3), validators.length(max=50)])
    username = StringField("Your username", [validators.Length(min=3), validators.length(max=50)])
    password = PasswordField("Password", [validators.Length(min=3), validators.length(max=50)])
    
    class Meta:
        csrf = False