from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm
from application.auth.forms import SignupForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))  

@app.route("/auth/signup", methods = ["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signupform.html", form = SignupForm())

    form = SignupForm(request.form)
    
    if not form.validate():
        return render_template("auth/signupform.html", form = form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/signupform.html", form = form,
                               error = "This username is already taken")
        
    account = User(form.name.data, form.username.data, form.password.data, "USER")

    db.session().add(account)
    db.session().commit()
    
    return redirect(url_for("index"))