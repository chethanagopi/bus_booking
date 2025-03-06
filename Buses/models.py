from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    bus_id = db.Column(db.Integer, nullable=False)  # No ForeignKey, just storing the ID
    seat_number = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Booking {self.id} for {self.user_name} on Bus {self.bus_id}>"
