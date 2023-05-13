from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app, bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "login_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod 
    def save(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append (cls(user))
        return users
    
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True 
        one_user = User.get_by_email(data)

        if one_user:
            is_valid = False
            flash("Please Log In", 'registration')
        if len(data['first_name']) < 2:
            is_valid = False
            flash('First Name must be at least 2 characters', 'registration')
        if len(data['last_name']) < 2:
            is_valid = False
            flash('Last Name must be at least 2 characters', 'registration')
        if len(data['email']) == 0:
            is_valid = False
            flash('Email must be submitted', 'registration')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Invalid Email', 'registration')
        if len(data['password']) < 8:
            is_valid = False
            flash('Password Must Be at least 8 Characters', 'registration')
        if len(data['confirm_password']) < 8:
            is_valid = False
            flash('Password Must Be at least 8 Characters', 'registration')
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('Password does not match', 'registration')
        return is_valid
        
    @staticmethod
    def validate_login(data):
        one_user = User.get_by_email(data)

        if not one_user:
            flash('Invalid Credentials', 'login')
            return False
        if not bcrypt.check_password_hash(one_user.password, data['password']):
            flash('Invalid Credentails', 'login')
            return False 
        return one_user


        

        
