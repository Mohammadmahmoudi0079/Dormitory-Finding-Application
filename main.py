from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_login import LoginManager
from admin.admin import admin_blueprint
from shared_db.shared_db import db
from admin.dormDB import DormDB_modify_blueprint , init_app as admin_init_app
from detailed_search.detailed_search import detailed_search_blueprint, DS_results_blueprint, DD_page_blueprint
from user.user_enter import user_blueprint 
from user.models import User
from owner.owner import owner_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Dorm_App_DB.sqlite3'
    app.secret_key = "2024springProject"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

# Load the user from the session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    db.init_app(app)  # Initialize the shared db instance with the app

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(DormDB_modify_blueprint)
    app.register_blueprint(detailed_search_blueprint)
    app.register_blueprint(DS_results_blueprint)
    app.register_blueprint(DD_page_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(owner_blueprint)

    

    return app

app = create_app()

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables for all models
    app.run(debug=True)