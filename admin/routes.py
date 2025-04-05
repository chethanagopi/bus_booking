# routes.py
from flask import Blueprint, jsonify,request
from services import * # Import the service function
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import app,bcrypt

# Define the blueprint
bus_bp = Blueprint('bus_routes', __name__)
from app import db
@app.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    if not all([username,password]):
        return jsonify({"message":"required"}), 400
    hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
    new_user=User(username=username,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    try: 
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        # Fetch user from DB
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password is correct
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Invalid username or password"}), 401  # Unauthorized

        # Generate JWT token (Ensure identity is a string)
        access_token = create_access_token(identity=user.id)

        return jsonify({"message": "Generated successfully", "token": access_token}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return 500 for internal errors
    
@app.route("/protected-route", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Should return a string
    return jsonify({"message": "Access granted", "user_id": current_user}), 200


@bus_bp.route("/admin", methods=['GET'])
@jwt_required()
def hello_microservice():
    message = {"message": "Welcome to GRSMC buses"}
    return jsonify(message)

@bus_bp.route('/buses/<int:bus_id>', methods=['GET'])
def get_bus(bus_id):
    """Fetch a bus by ID."""
    bus = Bus.query.get(bus_id)
    if not bus:
        return jsonify({"error": "Bus not found"}), 404
    return jsonify(bus.to_dict())

@bus_bp.route('/fetch-buses', methods=['GET'])
@jwt_required()
def fetch_buses():
    return get_all_buses()

@bus_bp.route("/add", methods=['POST'])
def add_new_bus():
    try:
        data=request.get_json()
        print(data)
        response, code=add_bus(data)
        print(response.get_json())
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bus_bp.route("/update/<int:id>", methods=["PUT"])
def update_bus_data(id):
    try:
        data=request.get_json()
        bus_update=update_bus(data,id)
        return bus_update
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bus_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_bus_data(id):
    try:
        logger.debug("hi")
        bus=delete_bus(id)
        # logger.info(bus.json)
        return bus
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bus_bp.route("/schedule", methods=["GET"])
def get_all_buses():
    try:
        print("schedule")

        schedule=get_schedules()
        print(schedule)
        return schedule
    except Exception as e:
        return jsonify({"error":str(e)})
    
@bus_bp.route("add-schedule", methods=["POST"])
def add_schedule_data():
    try:
        data=request.get_json()
        schedule=post_schedule(data)
        return schedule
    except Exception as e:
        return jsonify({"error":str(e)})
    
@bus_bp.route("/user", methods=['POST'])  # Added missing leading "/"
def add_user_details():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400
        
        return post_user(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# =================================admin==============================
@bus_bp.route("/add/admin", methods=['POST'])
def post_addmin_details_():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400
        
        return post_admin_details(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bus_bp.route("/get/admin", methods=['GET'])
def get_all_admins_():
    return get_all_admins()

from flask import Blueprint, request, jsonify, current_app
@bus_bp.route('/user/<int:user_id>/upload_photo', methods=['POST'])
def upload_photo_route(user_id):
    try:
        file = request.files.get('photo')
        upload_folder = current_app.config['UPLOAD_FOLDER']
        response, status_code = upload_profile_photo(user_id, file, upload_folder)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500