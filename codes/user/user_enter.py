from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from user.models import User
from admin.models import user_application
from shared_db.shared_db import db

user_blueprint = Blueprint('user', __name__, template_folder='templates')


def init_app(app):
    db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(user_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=11)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, current_user


@user_blueprint.route('/user/login', methods=['GET', 'POST'])
def user_login():
    
    if current_user.is_authenticated:
        return redirect(url_for('user.book_dorm'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  
            flash('Login successful', 'success')

            
            next_page = request.args.get('next')
            dorm_id = request.args.get('dorm_id')
            owner_id = request.args.get('owner_id')

            
            if next_page:
                return redirect(next_page)
            
            else:
                if dorm_id and owner_id:
                    return redirect(url_for('user.book_dorm', dorm_id=dorm_id, owner_id=owner_id))
                return redirect(url_for('user.book_dorm'))

        else:
            flash('Invalid email or password', 'danger')

   
    return render_template('user/login.html', form=form)


from flask import request

@user_blueprint.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('user.book_dorm'))  
    
    form = RegistrationForm()
    if request.method == 'POST':

        user_approval = request.form['share_info']
        if user_approval=="on":
            user_approval=True
        else:
            user_approval=False

        user = User(
            user_name=form.name.data,
            user_surename=form.surname.data,
            user_email=form.email.data,
            user_phone_number=form.phone_number.data,
            user_approval=user_approval,
            user_is_active=True 
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('user.user_login'))
    
    return render_template('user/register.html', form=form)


@user_blueprint.route('/user/book_dorm')
@login_required
def book_dorm():
    
    dorm_id = session['dorm_id']
    owner_id = session['owner_id']
    new_application = user_application(user_id=current_user.user_id, dorm_id=dorm_id, owner_id=owner_id)
    db.session.add(new_application)
    db.session.commit()
    flash('Dorm booked successfully!', 'success')
    return render_template('user/book_dorm.html')

@user_blueprint.route('/user/logout')
def user_logout():
    logout_user()
    return redirect(url_for('user.user_login'))
