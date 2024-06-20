from shared_db.shared_db import db
from datetime import datetime


class dorms(db.Model):
    dorm_id = db.Column("id", db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    sex = db.Column(db.CHAR)
    price = db.Column(db.Integer)
    meal_number = db.Column(db.Integer)
    cleaning_plan = db.Column(db.Integer)
    room_population = db.Column(db.Integer)
    kitchen = db.Column(db.Boolean)
    laundry = db.Column(db.Boolean)
    park = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    studying_hall = db.Column(db.Boolean)
    stars = db.Column(db.Float)
    location = db.Column(db.String(300))
    capacity = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    latest_check_in = db.Column(db.Integer)
    latest_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,owner_id, name, state, sex, price, meal_number, cleaning_plan,
                 room_population, kitchen, laundry, park, wifi, studying_hall,
                 stars, location, capacity, availability, city, latest_check_in):
        self.name = name
        self.owner_id =owner_id
        self.state = state
        self.sex = sex
        self.price = price
        self.meal_number = meal_number
        self.cleaning_plan = cleaning_plan
        self.room_population = room_population
        self.kitchen = kitchen
        self.laundry = laundry
        self.park = park
        self.wifi = wifi
        self.studying_hall = studying_hall
        self.stars = stars
        self.location = location
        self.capacity = capacity
        self.availability = availability
        self.city = city
        self.latest_check_in = latest_check_in

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class admin(db.Model,UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable= False)
    admin_surename = db.Column(db.String(50), nullable= False)
    admin_phone_number = db.Column(db.String(11), nullable= False)
    admin_email = db.Column(db.String(100), unique=True, nullable=False)
    admin_password_hash = db.Column(db.String(100), nullable=False)
    admin_is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class request_log(db.Model):
    __tablename__ = 'request_log'
    req_id = db.Column("id",db.Integer, primary_key=True)
    request_type = db.Column(db.String(50), nullable=False)
    request_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,request_type,request_id,created_at):

        self.request_type=request_type
        self.created_at=created_at
        self.request_id=request_id

class add_request(db.Model):
    __tablename__ = 'add_request'
    add_req_id = db.Column("id",db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    sex = db.Column(db.CHAR)
    price = db.Column(db.Integer)
    meal_number = db.Column(db.Integer)
    cleaning_plan = db.Column(db.Integer)
    room_population = db.Column(db.Integer)
    kitchen = db.Column(db.Boolean)
    laundry = db.Column(db.Boolean)
    park = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    studying_hall = db.Column(db.Boolean)
    stars = db.Column(db.Float)
    location = db.Column(db.String(300))
    capacity = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    latest_check_in = db.Column(db.Integer)
    latest_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,owner_id, name, state, sex, price, meal_number, cleaning_plan,
                 room_population, kitchen, laundry, park, wifi, studying_hall,
                 stars, location, capacity, availability, city, latest_check_in):
        self.name = name
        self.state = state
        self.owner_id=owner_id
        self.sex = sex
        self.price = price
        self.meal_number = meal_number
        self.cleaning_plan = cleaning_plan
        self.room_population = room_population
        self.kitchen = kitchen
        self.laundry = laundry
        self.park = park
        self.wifi = wifi
        self.studying_hall = studying_hall
        self.stars = stars
        self.location = location
        self.capacity = capacity
        self.availability = availability
        self.city = city
        self.latest_check_in = latest_check_in


class update_request(db.Model):
    __tablename__ = 'update_request'
    update_req_id = db.Column("id",db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    meal_number = db.Column(db.Integer)
    cleaning_plan = db.Column(db.Integer)
    room_population = db.Column(db.Integer)
    kitchen = db.Column(db.Boolean)
    laundry = db.Column(db.Boolean)
    park = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    studying_hall = db.Column(db.Boolean)
    
    def __init__(self, dorm_id, price, meal_number, cleaning_plan, room_population, kitchen, laundry, park, wifi, studying_hall,availability):
        self.dorm_id = dorm_id
        self.price = price
        self.meal_number = meal_number
        self.cleaning_plan = cleaning_plan
        self.room_population = room_population
        self.kitchen = kitchen
        self.laundry = laundry
        self.park = park
        self.wifi = wifi
        self.availability=availability
        self.studying_hall = studying_hall

class delete_request(db.Model):
    __tablename__ = 'delete_request'
    delete_req_id = db.Column("id",db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer)
    
    def __init__(self, dorm_id):
        self.dorm_id = dorm_id

class user_application(db.Model):
    __tablename__ = 'user_application'
    app_id = db.Column("id",db.Integer, primary_key=True)
    app_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer)
    dorm_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    
    def __init__(self, user_id, dorm_id,owner_id):
        self.user_id = user_id
        self.dorm_id = dorm_id
        self.owner_id =owner_id

class approved_request(db.Model):
    __tablename__ = "approved_request"
    approv_id = db.Column("id",db.Integer, primary_key=True)
    approved_req_id = db.Column(db.Integer)
    approve_dorm_id = db.Column(db.Integer)
    approve_owner_id = db.Column(db.Integer)
    approve_date = db.Column(db.DateTime, default=datetime.utcnow)
    def __init__(self, approve_dorm_id,approve_owner_id, approved_req_id):
        self.approve_dorm_id=approve_dorm_id
        self.approve_owner_id=approve_owner_id
        self.approved_req_id=approved_req_id
