from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import datetime

db = "ohana_rideshare"

class Ride:
    def __init__(self, data):
        self.id = data["id"]
        self.destination = data["destination"]
        self.pickup = data["pickup"]
        self.date = data["date"]
        self.details = data["details"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.driver_id = data["driver_id"]
        self.passenger_id = data["passenger_id"]
        self.passenger = []
        self.driver = []

    @staticmethod
    def validate_ride(data):
        is_valid = True

        #validate destination
        if len(data["destination"]) < 1:
            flash("Destination required", "destination")
            is_valid = False
        elif len(data["destination"]) < 3:
            flash("Destination must be at least 3 characters", "destination")
            is_valid = False

        #validate pickup location
        if len(data["pickup"]) < 1:
            flash("Pickup location required", "pickup")
            is_valid = False
        elif len(data["pickup"]) < 3:
            flash("Pickup location must be at least 3 pickup", "pickup")
            is_valid = False

        #validate rideshare date
        # today = datetime.datetime.now().strftime('%Y-%m-%d')
        # today_date = datetime.datetime.strptime(today,'%Y-%m-%d')
        # ride_date = datetime.datetime.strptime(data["date"], '%Y-%m-%d')
        if len(data["date"]) < 1:
            flash("Rideshare date required", "date")
            is_valid = False
        # elif ride_date < today_date:
        #     flash("Rideshare date cannot be in the past", "date")
        #     is_valid = False

        #validate details
        if len(data["details"]) < 1:
            flash("Details required", "details")
            is_valid = False
        elif len(data["details"]) < 10:
            flash("Details must be at least 10 characters", "details")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_ride_edit(data):
        is_valid = True

        #validate pickup location
        if len(data["pickup"]) < 1:
            flash("Pickup location required", "pickup")
            is_valid = False
        elif len(data["pickup"]) < 3:
            flash("Pickup location must be at least 3 pickup", "pickup")
            is_valid = False

        #validate details
        if len(data["details"]) < 1:
            flash("Details required", "details")
            is_valid = False
        elif len(data["details"]) < 10:
            flash("Details must be at least 10 characters", "details")
            is_valid = False

        return is_valid
    
    @classmethod
    def insert_ride(cls, data):
        query = '''
            INSERT INTO rides (destination, pickup, date, details, driver_id, passenger_id)
            VALUES(%(destination)s, %(pickup)s, %(date)s, %(details)s, %(driver_id)s, %(passenger_id)s);
        '''
        connectToMySQL(db).query_db(query, data)   
    
    @classmethod
    def get_all_with_passenger_and_driver(cls):
        query = '''
            SELECT * 
            FROM rides R
            LEFT JOIN users UP ON UP.id = R.passenger_id
            LEFT JOIN users UD ON UD.id = R.driver_id;
        '''
        results = connectToMySQL(db).query_db(query)
        rides = []
        for row in results:
            ride_obj = cls(row)
            passenger_info = {
                "id" : row["UP.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["UP.created_at"],
                "updated_at" : row["UP.updated_at"]
            }
            ride_obj.passenger = user.User(passenger_info)
            driver_info = {
                "id" : row["UD.id"],
                "first_name" : row["UD.first_name"],
                "last_name" : row["UD.last_name"],
                "email" : row["UD.email"],
                "password" : row["UD.password"],
                "created_at" : row["UD.created_at"],
                "updated_at" : row["UD.updated_at"]
            }
            ride_obj.driver = user.User(driver_info)
            rides.append(ride_obj)
        return rides
    
    @classmethod
    def get_one_with_passenger_and_driver(cls, data):
        query = '''
            SELECT * 
            FROM rides R
            LEFT JOIN users UP ON UP.id = R.passenger_id
            LEFT JOIN users UD ON UD.id = R.driver_id
            WHERE R.id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        ride_obj = cls(results[0])
        for row in results:
            passenger_info = {
                "id" : row["UP.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["UP.created_at"],
                "updated_at" : row["UP.updated_at"]
            }
            ride_obj.passenger = user.User(passenger_info)
            driver_info = {
                "id" : row["UD.id"],
                "first_name" : row["UD.first_name"],
                "last_name" : row["UD.last_name"],
                "email" : row["UD.email"],
                "password" : row["UD.password"],
                "created_at" : row["UD.created_at"],
                "updated_at" : row["UD.updated_at"]
            }
            ride_obj.driver = user.User(driver_info)
        return ride_obj
    
    @classmethod
    def update_rides_driver(cls, data):
        query = '''
            UPDATE rides
            SET driver_id = %(driver_id)s
            WHERE id = %(id)s;
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete_ride(cls, data):
        query = '''
            DELETE FROM rides
            WHERE id = %(id)s;
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_ride_pickup_details(cls, data):
        query = '''
            UPDATE rides
            SET pickup = %(pickup)s,
                details = %(details)s
            WHERE id = %(id)s;
        '''
        connectToMySQL(db).query_db(query, data)