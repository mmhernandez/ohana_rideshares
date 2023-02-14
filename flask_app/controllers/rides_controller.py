from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, rides


@app.route("/dashboard")
def dashboard():
    if "id" in session:
        logged_in_user_info = user.User.get_user_by_id({"id": session["id"]})

        rides_list = rides.Ride.get_all_with_passenger_and_driver()

        return render_template("dashboard.html", user=logged_in_user_info, rides=rides_list)
    return redirect("/")

@app.route("/rides/new")
def request_ride():
    if "id" in session:
        return render_template("request_ride.html")
    return redirect("/")

@app.route("/add_ride", methods=["POST"])
def insert_ride():
    if "id" in session:
        ride_data = {
            "destination": request.form["destination"],
            "pickup": request.form["pickup"],
            "date": request.form["date"],
            "details": request.form["details"],
            "driver_id": None,
            "passenger_id": session["id"]
        }
        print(f"ride_data = {ride_data}")
        if rides.Ride.validate_ride(ride_data):
            rides.Ride.insert_ride(ride_data)
            if "destination" in session:
                session.pop("destination")
            if "pickup" in session:
                session.pop("pickup")
            if "date" in session:
                session.pop("date")
            if "details" in session:
                session.pop("details")   
            return redirect("/dashboard")
        else:
            session["destination"] = ride_data["destination"]
            session["pickup"] = ride_data["pickup"]
            session["date"] = ride_data["date"]
            session["details"] = ride_data["details"]
            return redirect("/rides/new")
    return redirect("/")

@app.route("/cancel_ride")
def cancel_ride_request():
    if "id" in session:
        if "destination" in session:
            session.pop("destination")
        if "pickup" in session:
            session.pop("pickup")
        if "date" in session:
            session.pop("date")
        if "details" in session:
            session.pop("details") 
        return redirect("/dashboard")
    return redirect("/")

@app.route("/cancel_request/<int:id>")
def cancel_ride_by_id(id):
    if "id" in session:
        #delete ride
        return redirect("/dashboard")
    return redirect("/")

@app.route("/add_driver/<int:id>")
def assign_driver(id):
    if "id" in session:
        ride_info = {
            "id" : id,
            "driver_id" : session["id"]
        }
        rides.Ride.update_rides_driver(ride_info)
        return redirect("/dashboard")
    return redirect("/")

@app.route("/driver_cancellation/<int:id>")
def cancel_driver(id):
    if "id" in session:
        ride_info = {
            "id" : id,
            "driver_id" : None
        }
        rides.Ride.update_rides_driver(ride_info)
        return redirect("/dashboard")
    return redirect("/")

@app.route("/rides/<int:id>")
def view_ride(id):
    if "id" in session:
        return render_template("view_ride.html")
    return redirect("/")