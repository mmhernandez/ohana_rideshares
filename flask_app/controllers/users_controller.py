from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user

@app.route("/")
def login_registration():
    return render_template("login_registration.html")

@app.route("/register", methods=["POST"])
def register():
    registration_info = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["em"],
        "password": request.form["pw"],
        "confirm_password": request.form["confirm_pw"]
    }
    if user.User.validate_registration(registration_info):
        session["id"] = user.User.insert_user(registration_info)
        return redirect("/dashboard")
    else:
        session["first_name"] = registration_info["first_name"]
        session["last_name"] = registration_info["last_name"]
        session["email"] = registration_info["email"]
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    login_info = {
        "email": request.form["email"],
        "password": request.form["pw"]
    }
    if user.User.validate_login(login_info):
        logged_in_user = user.User.get_user_by_email(login_info)
        session["id"] = logged_in_user.id
        return redirect("/dashboard")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")