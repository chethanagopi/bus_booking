from app import app,db
from routes import *

app.register_blueprint(bp,)
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080,debug=True)