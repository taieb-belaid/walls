from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(): 
    def __init__(self,data) :
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated = data['updated_at']
    
    @classmethod
    def get_user_by_mail(cls,data):
        query ="select * from users where email = %(email)s"
        result = connectToMySQL('walls_schema').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def valid_registration(user):
        user_in_db = User.get_user_by_mail(user)
        is_valid = True
        if len(user['first_name']) < 2:
            flash('first name must a least have 2 characters')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('last name must at least have 2 characters')
            is_valid = False
        if len(user['password']) < 8:
            flash('password must a least have 8 characters')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('email invalid')
            is_valid=False    
        if not user['password'] == user['confirm_password']:
            flash('password should match')
            is_valid = False
        if user_in_db:
            flash('email already exist')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        new_dict={
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' :bcrypt.generate_password_hash( data['password'])
        }
        query ='INSERT INTO users(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);'
        return connectToMySQL('walls_schema').query_db(query,new_dict)

    @classmethod
    def get_user_by_id(cls,data):
        query ='select * from users where id = %(id)s'
        result= connectToMySQL('walls_schema').query_db(query,data) 
        return cls(result[0])

    @classmethod
    def get_all_users(cls,data):
        query ='SELECT * FROM users WHERE users.id NOT IN (%(id)s) ;'
        results = connectToMySQL('walls_schema').query_db(query,data)
        return results
