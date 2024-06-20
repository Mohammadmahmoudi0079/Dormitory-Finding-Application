from flask import Blueprint,session, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import LoginManager, login_user, current_user,logout_user ,login_required
from owner.models import owner
from user.models import User
from admin.models import dorms,add_request,request_log,update_request,delete_request,user_application
from shared_db.shared_db import db
import json
from datetime import datetime

owner_blueprint = Blueprint('owner', __name__, template_folder='templates')

def init_app(app):
    db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'owner.login'
login_manager.session_protection = "strong"
login_manager.init_app(owner_blueprint)

@login_manager.user_loader
def load_owner(owner_id):
    return owner.query.get(int(owner_id))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    owner_name = StringField('Name', validators=[DataRequired()])
    owner_surename = StringField('Surname', validators=[DataRequired()]) 
    owner_phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=11, max=11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@owner_blueprint.route('/owner/owner_enter', methods=['GET', 'POST'])
def owner_enter():
    return render_template('owner/owner_enter.html')

@owner_blueprint.route('/owner/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('owner.ownerUI'))  
    
    form = LoginForm()
    if form.validate_on_submit():
        owner_instance = owner.query.filter_by(owner_email=form.email.data).first()
        if owner_instance and owner_instance.check_password(form.password.data):

            login_user(owner_instance)  

            session['owner_id'] = owner_instance.owner_id
            flash('Login successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('owner.ownerUI'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('owner/login.html', form=form)

@owner_blueprint.route('/owner/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('owner.ownerUI')) 
    
    form = RegistrationForm()
    if form.validate_on_submit():
        owner_instance = owner(
            owner_name=form.owner_name.data,
            owner_surename=form.owner_surename.data, 
            owner_phone_number=form.owner_phone_number.data,
            owner_email=form.email.data
        )
        owner_instance.set_password(form.password.data)
        db.session.add(owner_instance)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('owner.login'))
    return render_template('owner/register.html', form=form)

@owner_blueprint.route('/owner/logout')

def owner_logout():
    logout_user()
    return redirect(url_for('owner.owner_enter'))

@owner_blueprint.route('/owner/ownerUI', methods=['GET', 'POST'])
@login_required
def ownerUI():
    return render_template("/owner/ownerUI.html")


@owner_blueprint.route("/owner/add_dorm", methods=['GET', 'POST'])
def add_dorm():
    if request.method == 'POST':
        
        try:
            name = request.form['name']
            state = request.form['state']
            city = request.form['city']
            sex = request.form['sex']
            price = int(request.form['price'])
            meal_number = int(request.form['meal_number'])
            cleaning_plan = int(request.form['cleaning_plan'])
            room_population = int(request.form['room_population'])
            kitchen = request.form.get('kitchen') == 'on'
            laundry = request.form.get('laundry') == 'on'
            park = request.form.get('park') == 'on'
            wifi = request.form.get('wifi') == 'on'
            studying_hall = request.form.get('studying_hall') == 'on'
            stars = float(request.form['stars'])
            location = request.form['location']
            capacity = int(request.form['capacity'])
            availability = int(request.form['availability'])
            latest_check_in = int(request.form['latest_check_in'])

            owner_id = session.get('owner_id')
            
            new_dorm = add_request(name=name,owner_id=owner_id, state=state, city=city, sex=sex, price=price, meal_number=meal_number,
                             cleaning_plan=cleaning_plan, room_population=room_population, kitchen=kitchen,
                             laundry=laundry, park=park, wifi=wifi, studying_hall=studying_hall,
                             stars=stars, location=location, capacity=capacity, availability=availability,
                             latest_check_in=latest_check_in)

            db.session.add(new_dorm)
            db.session.commit()
            log_entry = request_log(
                request_type='add',
                request_id=new_dorm.add_req_id,
                created_at=datetime.utcnow()
            )
            db.session.add(log_entry)
            db.session.commit()
            return render_template("owner/dorm_added.html", success=True, dorm=new_dorm)
        except Exception as e:
            flash('Failed to add dorm: ' + str(e), 'danger')
            return render_template("owner/dorm_added.html", success=False, error=str(e))

    with open('./data/state_and_cities.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template("owner/add_dorm.html", data=data)


@owner_blueprint.route("/owner/modify_dorm", methods=['GET', 'POST'])
def modify_dorm():
    dorm = None
    if request.method == 'POST':
        action = request.form.get('action')
        owner_id = session.get('owner_id')
        if action == 'search':
            dorm_name = request.form.get('dorm_name', '').strip()
            dorm = dorms.query.filter(dorms.name.ilike(f"%{dorm_name}%"), dorms.owner_id == owner_id).first()
            if not dorm:
                flash('Dorm not found', 'error')

        elif action in ['update', 'delete']:
            dorm_id = request.form.get('dorm_id')
            dorm = dorms.query.get(dorm_id)
            if dorm:
                if action == 'update':
                    
                    update_req = update_request(
                        dorm_id=dorm_id,
                        availability = int(request.form.get('availability')),
                        price=int(request.form.get('price')),
                        meal_number=int(request.form.get('meal_number')),
                        cleaning_plan=int(request.form.get('cleaning_plan')),
                        room_population=int(request.form.get('room_population')),
                        kitchen=request.form.get('kitchen') == 'on',
                        laundry=request.form.get('laundry') == 'on',
                        park=request.form.get('park') == 'on',
                        wifi=request.form.get('wifi') == 'on',
                        studying_hall=request.form.get('studying_hall') == 'on'
                    )
                    db.session.add(update_req)
                    db.session.commit()
                    flash('Update request logged successfully', 'success')
                    log_entry = request_log(
                    request_type='update',
                    request_id= update_req.update_req_id,
                    created_at=datetime.utcnow()
                    )   
                    db.session.add(log_entry)
                    db.session.commit()

                elif action == 'delete':
                    
                    delete_req = delete_request(dorm_id=dorm_id)
                    db.session.add(delete_req)
                    db.session.commit()
                    flash('Delete request logged successfully', 'success')
                    log_entry = request_log(
                    request_type='delete',
                    request_id=delete_req.delete_req_id,
                    created_at=datetime.utcnow()
                    )
                    db.session.add(log_entry)
                    db.session.commit()

                
                return redirect(url_for('owner.modify_dorm'))  
            else:
                flash('Dorm not found during action', 'error')

    return render_template('owner/modify_dorm.html', dorm=dorm)

@owner_blueprint.route("/owner/book_request", methods=['GET', 'POST'])
def book_request():
    owner_id = session.get('owner_id')
    request = user_application.query.filter_by(owner_id=owner_id).all()
    user_details = {}  
    for req in request:
        user_instance = User.query.get(req.user_id)
        if user_instance:
            user_details[req.user_id] = {
                'req_id' : req.app_id,
                'name': user_instance.user_name,
                'surname': user_instance.user_surename,
                'email': user_instance.user_email,
                'phone_number': user_instance.user_phone_number
            }
            
    return render_template("owner/book_request.html",user_details=user_details)

@owner_blueprint.route('/owner/delete_book_request/<int:req_id>', methods=['POST'])
def delete_book_request(req_id):
    request_to_delete = user_application.query.get_or_404(req_id)
    try:
        db.session.delete(request_to_delete)
        db.session.commit()
        flash('Request deleted successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error deleting request.', 'error')
    return redirect(url_for('owner.book_request'))