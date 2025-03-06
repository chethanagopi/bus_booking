from flask_sqlalchemy import SQLAlchemy
from app import db  # Assuming you have a 'db' object initialized in 'app.py'

class Bus(db.Model):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    bus_type = db.Column(db.String(50), nullable=False)  # e.g., AC, Non-AC, Sleeper, Semi-Sleeper
    total_seats = db.Column(db.Integer, nullable=False)
    operator = db.Column(db.String(100), nullable=False)

    schedules = db.relationship('Schedule', backref='bus', lazy=True)
    def to_dict(self):
        return{"id":self.id,
               "bus_number":self.bus_number,
               "bus_type":self.bus_type,
               "total_seats":self.total_seats,
               "operator":self.operator}

    def __repr__(self):
        return f"<Bus {self.bus_number} - {self.bus_type}>"
    

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    fare = db.Column(db.Float, nullable=False)

    # Relationship to Bookings
    bookings = db.relationship('Booking', backref='schedule', lazy=True)

    def __repr__(self):
        return f"<Schedule {self.source} to {self.destination} at {self.departure_time}>"
    def to_dict(self):
        return {"id":self.id,
                "bus_id":self.bus_id,
                "source":self.source,
                "destination":self.destination,
                "departure_time":self.departure_time,
                "arrival_time":self.arrival_time,
                "fare":self.fare}
        

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False)

    # No need to define the relationship again, it's already defined in Schedule
    # schedule = db.relationship('Schedule', backref='bookings', lazy=True)

    def __repr__(self):
        return f"<Booking {self.customer_name} at {self.booking_time}>"
    
class User(db.Model):
    __tablename__='users'
    # id=db.Column(db.Integer,primary_Key=True,autoincrement=True)
    id = db.Column(db.String, primary_key=True, autoincrement=True)

    username=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(250),nullable=False)
    def to_dict(self):
        return{"id":self.id,
               "username":self.username,"password":self.password
        }