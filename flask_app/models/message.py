from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ride, user
from flask import flash

db = db = "ohana_rideshare"

class Message:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.ride_id = data["ride_id"]
        self.sender_id = data["sender_id"]
        self.recipient_id = data["recipient_id"]
        self.ride = None
        self.sender = None
        self.recipient = None
    
    @classmethod
    def insert_message(cls, data):
        query = '''
            INSERT INTO messages (content, ride_id, sender_id, recipient_id)
            VALUES (%(content)s, %(ride_id)s, %(sender_id)s, %(recipient_id)s);
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_by_ride_with_sender_recipient(cls, data):
        query = '''
            SELECT *
            FROM messages M
            RIGHT OUTER JOIN rides R on M.ride_id = R.id
            LEFT JOIN users US ON M.sender_id = US.id
            LEFT JOIN users UR ON M.recipient_id = UR.id
            WHERE R.id = %(id)s
            ORDER BY M.created_at;
        '''
        results = connectToMySQL(db).query_db(query, data)
        messages = []
        for row in results:
            message_obj = cls(row)
            ride_info = {
                "id" : row["R.id"],
                "destination" : row["destination"],
                "pickup" : row["pickup"],
                "date" : row["date"],
                "details" : row["details"],
                "created_at" : row["R.created_at"],
                "updated_at" : row["R.updated_at"],
                "driver_id" : row["driver_id"],
                "passenger_id" : row["passenger_id"]
            }
            message_obj.ride = ride.Ride(ride_info)
            sender_info = {
                "id" : row["US.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["US.created_at"],
                "updated_at" : row["US.updated_at"]
            }
            message_obj.sender = user.User(sender_info)
            recipient_info = {
                "id" : row["UR.id"],
                "first_name" : row["UR.first_name"],
                "last_name" : row["UR.last_name"],
                "email" : row["UR.email"],
                "password" : row["UR.password"],
                "created_at" : row["UR.created_at"],
                "updated_at" : row["UR.updated_at"]
            }
            message_obj.recipient = user.User(recipient_info)
            messages.append(message_obj)
        return messages
    