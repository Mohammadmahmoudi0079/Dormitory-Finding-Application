from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from shared_db.shared_db import db

class User(db.Model,UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable= False)
    user_surename = db.Column(db.String(50), nullable= False)
    user_phone_number = db.Column(db.String(11), nullable= False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password_hash = db.Column(db.String(100), nullable=False)
    user_approval = db.Column(db.Boolean, default =False)
    user_is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.user_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password_hash, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return str(self.user_id)
