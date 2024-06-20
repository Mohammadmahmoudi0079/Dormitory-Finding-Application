from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

db = SQLAlchemy()

from . import admin, models
