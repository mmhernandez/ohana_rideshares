from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ride, user
from flask import flash

db = "ohana_rideshare"

class Message:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.ride_id = data["ride_id"]
        self.user_id = data["user_id"]
        self.ride = None
        self.user = None
    
    @classmethod
    def insert_message(cls, data):
        query = '''
            INSERT INTO messages (content, ride_id, user_id)
            VALUES (%(content)s, %(ride_id)s, %(user_id)s);
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_by_ride_with_ride_user(cls, data):
        query = '''
            SELECT *
            FROM messages M
            RIGHT OUTER JOIN rides R on M.ride_id = R.id
            LEFT JOIN users U ON M.user_id = U.id
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
            user_info = {
                "id" : row["U.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["U.created_at"],
                "updated_at" : row["U.updated_at"]
            }
            message_obj.sender = user.User(user_info)
            messages.append(message_obj)
        return messages
    