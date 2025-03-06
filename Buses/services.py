import requests

ADMIN_SERVICE_URL = "http://127.0.0.1:5000"  # Replace with actual service URL

def fetch_bus_details(bus_id):
    """Fetch bus details from the admin service."""
    url = f"{ADMIN_SERVICE_URL}/buses/{bus_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return None