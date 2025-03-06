import requests
from app import app
from flask import Blueprint, jsonify

bp=Blueprint("buses",__name__,url_prefix="/member")
# ADMIN_SERVICE_URL = "http://127.0.0.1:5000/bus_routes/fetch-buses"  # Replace with actual Admin service URL



# def call_random_microservie():
#     response = requests.get(ADMIN_SERVICE_URL)
#     return response.json().get("data")

# @buses_bp.route('/fetch-admin-data', methods=['GET'])
# def fetch_admin_data():
#     """Fetch data from the Admin service."""
#     try:
#         random_number = call_random_microservie()

#         return random_number, 200
#         return jsonify({"error": "Failed to fetch data from Admin service"}), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Admin service unavailable", "details": str(e)}), 500


import requests
from flask import jsonify

random_microservice_url = "http://127.0.0.1:5000/bus_routes/schedule"
login_url = "http://127.0.0.1:5000/login"

 # Use a valid registered password
username = "papu"
password = "papu112"

def get_jwt_token():
    credentials = {"username" : username , "password" : password}
    try:
        response=requests.post(login_url,json=credentials)
        response.raise_for_status()

        token=response.json().get("token")
        if token:
            return token
        else:
            return None
    except Exception as e:
      return jsonify({e})



def call_random_microservice():
    """Call /generate endpoint with JWT authentication"""
    token = get_jwt_token()
    if not token:
        print("Failed to retrieve JWT token")
        return None

    headers = {"Authorization": f"Bearer {token}"}  # Include JWT token
    try:
        response = requests.get(random_microservice_url, headers=headers, timeout=5)
        response.raise_for_status()  # Raises error for HTTP 4xx/5xx
        
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random number: {e}")
        return None



@app.route("/buses",methods=['GET'])
def get_all_buses():
    try:
      random_number = call_random_microservice()
      return jsonify({"data":random_number})
    except Exception as e:
      return jsonify({e})


