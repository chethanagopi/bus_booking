# run.py
from app import app  # Import `app` from `app.py`
from routes import bus_bp  # Import the blueprint from `routes.py`

# Register the blueprint
app.register_blueprint(bus_bp, url_prefix='/bus_routes')
# Run the application
if __name__ == '__main__':
    app.run(debug=True)
