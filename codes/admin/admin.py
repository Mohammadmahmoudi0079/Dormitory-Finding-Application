from flask import Blueprint,session, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import LoginManager, login_user, current_user,logout_user
from owner.models import owner
from admin.models import dorms,add_request,request_log,update_request,delete_request,approved_request
from shared_db.shared_db import db
import json
from datetime import datetime

admin_blueprint = Blueprint("admin",__name__,static_folder="static",template_folder="admin")

@admin_blueprint.route('/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['admin_login_password']
        
        if password == 'adminPass':
            session['logged_in'] = True
            return redirect(url_for('admin.admin'))  
        else:
            flash("Invalid password.", "error")
            return redirect(url_for('admin.login'))  
    return render_template('admin/admin_login.html')  
@admin_blueprint.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))  
    return render_template('admin/admin.html')

@admin_blueprint.route("/admin_logout")
def logout():
    session['logged_in']=False
    return redirect(url_for("admin.login"))



@admin_blueprint.route('/admin/requests')
def view_requests():
    requests = request_log.query.all()
    return render_template('admin/requests.html', requests = requests)


@admin_blueprint.route('/admin/request_detail/<int:req_id>/<string:req_type>',methods=['GET', 'POST'])
def request_detail(req_id, req_type):
    if req_type == "update":
        request_data = update_request.query.filter_by(update_req_id=req_id).first()
    elif req_type == "delete":
        request_data = delete_request.query.filter_by(delete_req_id=req_id).first()
    elif req_type == "add":
        request_data = add_request.query.filter_by(add_req_id=req_id).first()
    
    if not request_data:
        flash('Request not found', 'error')
        return redirect(url_for('admin.view_requests'))

    return render_template('admin/request_detail.html', request_data=request_data, req_type=req_type)

@admin_blueprint.route('/admin/approve_req/<int:req_id>/<string:req_type>', methods=['GET', 'POST'])
def approve_req(req_id, req_type):
    my_request = request_log.query.filter_by(request_id=req_id).first()
    if request.method == 'POST':
        my_request = request_log.query.filter_by(request_id=req_id).first()
        if req_type == 'update':

            update_request_data = update_request.query.get(req_id)
            if update_request_data:

                dorm_to_update = dorms.query.get(update_request_data.dorm_id)
                if (dorm_to_update):
                    update_request_data.price
                    dorm_to_update.price = update_request_data.price
                    dorm_to_update.meal_number = update_request_data.meal_number
                    dorm_to_update.cleaning_plan = update_request_data.cleaning_plan
                    dorm_to_update.room_population = update_request_data.room_population
                    dorm_to_update.kitchen = update_request_data.kitchen
                    dorm_to_update.availability = update_request_data.availability
                    dorm_to_update.laundry = update_request_data.laundry
                    dorm_to_update.park = update_request_data.park
                    dorm_to_update.wifi = update_request_data.wifi
                    dorm_to_update.studying_hall = update_request_data.studying_hall
                    db.session.commit()
                    flash('Update request approved successfully', 'success')
                
                
                    approved_entry = approved_request(
                        approve_dorm_id= dorm_to_update.dorm_id,
                        approve_owner_id=dorm_to_update.owner_id,
                        approved_req_id=my_request.req_id
                    )
                    db.session.add(approved_entry)
                    db.session.commit()
                else:
                    flash('can not update since dorm does not exist','error')
        elif req_type == 'delete':
            delete_item = request_log.query.get(req_id)
            delete_request_data = delete_request.query.get(delete_item.req_id)
            if delete_request_data:
                dorm_to_delete = dorms.query.get(delete_request_data.dorm_id)
                if dorm_to_delete:
                    db.session.delete(dorm_to_delete)
                    approved_entry = approved_request(
                        approve_dorm_id= dorm_to_delete.dorm_id,
                        approve_owner_id=dorm_to_delete.owner_id,
                        approved_req_id=my_request.req_id
                    )
                    db.session.add(approved_entry)
                    db.session.commit()
                    flash('Delete request approved successfully','success')
                else:
                    flash('Dorm dose not exist in the DB','error')
        elif req_type == 'add':
            
            add_request_data = add_request.query.get(req_id)
            if add_request_data:
                existing_dorm = dorms.query.filter_by(name=add_request_data.name).first()
                if existing_dorm:
                     flash(f'A dorm with the name "{add_request_data.name}" already exists.', 'error')
                else:
                    new_dorm = dorms(
                        name=add_request_data.name,
                        state=add_request_data.state,
                        city=add_request_data.city,
                        owner_id=add_request_data.owner_id,
                        sex=add_request_data.sex,
                        price=add_request_data.price,
                        meal_number=add_request_data.meal_number,
                        cleaning_plan=add_request_data.cleaning_plan,
                        room_population=add_request_data.room_population,
                        kitchen=add_request_data.kitchen,
                        laundry=add_request_data.laundry,
                        park=add_request_data.park,
                        wifi=add_request_data.wifi,
                        studying_hall=add_request_data.studying_hall,
                        stars=add_request_data.stars,
                        location=add_request_data.location,
                        capacity=add_request_data.capacity,
                        availability=add_request_data.availability,
                        latest_check_in=add_request_data.latest_check_in
                    )
                    db.session.add(new_dorm)
                    db.session.commit()
                    new_dorm = dorms.query.filter_by(name=new_dorm.name).first()
                    approved_entry = approved_request(
                    approve_dorm_id= new_dorm.dorm_id,
                    approve_owner_id=new_dorm.owner_id,
                    approved_req_id=my_request.req_id
                    )
                    db.session.add(approved_entry)
                    db.session.commit()
                    flash('Add request approved successfully', 'success')

        
        return redirect(url_for('admin.view_requests'))

    return render_template('admin/approve_req.html', req_id=req_id, req_type=req_type,request_id=my_request.request_id)


@admin_blueprint.route('/delete_request_from_list/<int:req_id>', methods=['POST'])
def delete_request_from_list(req_id):
    request_to_delete = request_log.query.get_or_404(req_id)
    try:
        db.session.delete(request_to_delete)
        db.session.commit()
        flash('Request deleted successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error deleting request.', 'error')
    return redirect(url_for('admin.view_requests'))

@admin_blueprint.route('/delete_approval_from_list/<int:req_id>', methods=['POST'])
def delete_approval_from_list(req_id):
    approval_to_delete = approved_request.query.filter_by(approved_req_id=req_id).first()
    try:
        db.session.delete(approval_to_delete)
        db.session.commit()
        flash('Request deleted successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error deleting request.', 'error')
    return redirect(url_for('admin.approved_req'))


@admin_blueprint.route('/admin/approved_req')
def approved_req():
    approved_items = approved_request.query.all()
    return render_template("admin/approved_req.html",approved_items=approved_items)



