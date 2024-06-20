from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from shared_db.shared_db import db

class owner(db.Model,UserMixin):
    owner_id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(50), nullable= False)
    owner_surename = db.Column(db.String(50), nullable= False)
    owner_phone_number = db.Column(db.String(11), nullable= False)
    owner_email = db.Column(db.String(100), unique=True, nullable=False)
    owner_password_hash = db.Column(db.String(100), nullable=False)
    owner_is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.owner_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.owner_password_hash, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return str(self.owner_id)