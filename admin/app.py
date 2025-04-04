import logging
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,verify_jwt_in_request
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chethana:Pavan6458%40@localhost:3306/chethana'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
import os
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from a .env file

# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
app.config['JWT_SECRET_KEY'] = '9f6b1a3c7e8d5f2a4c6b0d1e9a7f3b2c1d4e8f5a6b7c0d9e3f2a1b4c6d7e8f9' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

EXCLUDED_ROUTES=['/login','/register']


def check_jwt():
    """Middleware to enforce JWT authentication on all routes except the excluded ones."""
    if request.path not in EXCLUDED_ROUTES:
        try:
            verify_jwt_in_request()  # This will raise an error if the token is invalid or missing
        except Exception as e:
            return jsonify({"message": "Missing or invalid token", "error": str(e)}), 401

from dotenv import load_dotenv
load_dotenv()

db_password = os.getenv("DB_PASSWORD")  
print(f"Database Password: {db_password}")
