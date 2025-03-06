from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,verify_jwt_in_request
from datetime import timedelta
db=SQLAlchemy()
jwt=JWTManager()
bcrypt=Bcrypt()
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost:3306/buses'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
