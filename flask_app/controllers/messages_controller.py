from flask_app import app
from flask import session, redirect, request
from flask_app.models import message

@app.route("/send_message/<int:ride_id>", methods=["POST"])
def add_message(ride_id):
    if "id" in session:
        message_info = {
            "content": request.form["message"],
            "ride_id": ride_id,
            "user_id": session["id"],
        }
        message.Message.insert_message(message_info)
        return redirect(f"/rides/{ride_id}")
    return redirect("/")
