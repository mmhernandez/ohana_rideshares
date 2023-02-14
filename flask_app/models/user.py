from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re

db = "ohana_rideshare"
bcrypt = Bcrypt(app)
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z ,.\'-]+$')
# password_regex = re.compile(r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[#$@!%&?])[A-Za-z\d#$@!%&?]{8,25}$')


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_registration(data):
        is_valid = True

        #first name validation
        if len(data["first_name"]) < 1:
            flash("First name required", "first_name")
            is_valid = False
        elif len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters", "first_name")
            is_valid = False
        elif not name_regex.match(data["first_name"]):
            flash("Invalid first name", "first_name")
            is_valid = False
        
        #last name validation
        if len(data["last_name"]) < 1:
            flash("Last name required", "last_name")
            is_valid = False
        elif len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters", "last_name")
            is_valid = False
        elif not name_regex.match(data["last_name"]):
            flash("Invalid last name", "last_name")
            is_valid = False

        #email validation
        if len(data["email"]) < 1:
            flash("Email required", "email")
            is_valid = False
        elif not email_regex.match(data["email"]):
            flash("Invalid email", "email")
            is_valid = False
        elif User.get_user_by_email(data):
            flash("Email already in use", "email")
            is_valid = False

        #password validation
        if len(data["password"]) < 1:
            flash("Password required", "password")
            is_valid = False
        elif len(data["password"]) < 8:
            flash("Password must be at least 8 characters", "password")
            is_valid = False
        # elif not password_regex.match(data["password"]):
        #     flash("Invalid password (password must contain at least one uppercase letter, one number, and one special character)", "password")
        #     is_valid = False
        elif data["password"] != data["confirm_password"]:
            flash("Passwords must match", "password")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_info = User.get_user_by_email(data)
        print(user_info.password)
        if not user_info:
            flash("Invalid email and/or password", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(user_info.password, data['password']):
            flash("Invalid email and/or password xxxx", "login")
            is_valid = False
        
        return is_valid

    @classmethod
    def get_user_by_email(cls, data):
        query = '''
            SELECT * 
            FROM users
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def insert_user(cls, data):
        query = '''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        '''
        hashed_password = bcrypt.generate_password_hash(data["password"])
        data.update({"password": hashed_password})
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_user_by_id(cls, data):
        query = '''
            SELECT *
            FROM users
            WHERE id = %(id)s
        '''
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])