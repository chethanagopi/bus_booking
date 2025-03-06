
import requests  
from models import *
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from utils.log_handler import get_logger
logger=get_logger()

def get_all_buses():
    try:
        buses = Bus.query.all()  # Fetch all buses
        
        if not buses:
            return jsonify({"message": "No buses found", "data": []}), 200

        buses_list = [bus.to_dict() for bus in buses]  # Convert objects to dictionaries

        return jsonify({"message": "success", "data": buses_list}), 200  # Always return a valid JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
def add_bus(data):
    try:
        if not data:
            return jsonify({"error":"invalid json data"}), 400
             
        bus_number=data.get('bus_number')
        bus_type=data.get('bus_type')
        total_seats=data.get('total_seats')
        operator=data.get('operator')  
        if not all([bus_number,bus_type,total_seats,operator]):
            return jsonify({"error":"missing some field"}), 400
        bus=db.session.query(Bus).filter_by(bus_number=bus_number).first()
        if bus:
            return jsonify({"message":"already exist"}), 409
        else:
            new_bus=Bus(
                bus_number=bus_number,
                bus_type=bus_type,
                total_seats=total_seats,
                operator=operator
            )
            db.session.add(new_bus)
            db.session.commit()
            print("bus",new_bus)
            bus_dict = {k: v for k, v in new_bus.__dict__.items() if not k.startswith("_")}
            print("bus_dict",bus_dict)
            return jsonify({"message": "Bus added successfully", "bus": bus_dict}), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error":"database errors"+str(e)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_bus(data,id):
    try:
        bus_number=data.get("bus_number")
        bus_type=data.get("bus_type")
        operator=data.get("operator")
        total_seats=data.get("total_seats")
        if not data:
            return jsonify({"message":"no fields to update"})
        bus=db.session.query(Bus).filter_by(id=id).first()
        if bus_number:
            bus.bus_number = bus_number
        if bus_type:
            bus.bus_type = bus_type
        if operator:
            bus.operator = operator
        if total_seats:
            bus.total_seats = total_seats
        db.session.commit()
        return jsonify({"message":"updated","data":bus.to_dict()}), 200
       
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error":"db errors"+ str(e)}), 500
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    
def delete_bus(id):
    try:
        bus=db.session.query(Bus).filter_by(id=id).first()
        if bus:
            db.session.delete(bus)
            db.session.commit()
            return jsonify({"message":"deleted"}),200
        else:
            return jsonify({"message":"no bus with {id}"}),404
    except SQLAlchemyError as e:
        return jsonify({"error":"errors"+str(e)})
    except Exception as e:
        logger.error(f"{e}")
        return None
    

def get_schedules():
    try:
        schedules=Schedule.query.all()
        if not schedules:
            return jsonify({"message":"no data found"}), 404
        else:
            schedule_list=[schedule.to_dict() for schedule in schedules]
            return jsonify({"message":"fetched","data":schedule_list}), 200
    except Exception as e:
        print(f"Error: {e}")  
        logger.error(str(e))  # ✅ Correct

        return jsonify({"message":"internal server error"}), 500
    
def post_schedule(data):
    try:
        bus_id=data.get("bus_id")
        source=data.get("source")
        destination=data.get("destination")
        departure_time=data.get("departure_time")
        arrival_time=data.get("arrival_time")
        fare=data.get("fare")
        if not all([bus_id,source,destination,departure_time,arrival_time,fare]):
            return jsonify({"message":"some fields are missing"}), 404
        else:
            schedule=Schedule(bus_id=bus_id,source=source,destination=destination,departure_time=departure_time,
                              arrival_time=arrival_time,fare=fare)
            schedule_list={k:l for k,l in schedule.__dict__.items() if not k.startswith("_")}
            db.session.add(schedule)
            db.session.commit()
            return jsonify({"message":"added successfuly","data":schedule_list})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error":"database errors"+str(e)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def post_user(data):
    try:
        username=data.get("username")
        password=data.get("password")
        if not all([username,password]):
            return jsonify({"message":"some missing"})
        else:
            user=User(username=username,password=password)
            user_list={k:l for k,l in user.__dict__.items() if not k.startswith('_')}
            db.session.add(user)
            db.session.commit()
            return jsonify({"message":"success","data":user_list})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error":str(e)})
    except Exception as e:
        return jsonify({"error":str(e)})



