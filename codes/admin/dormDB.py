from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from admin.models import dorms
from shared_db.shared_db import db

DormDB_modify_blueprint = Blueprint("DormDB_modify", __name__, static_folder="static", template_folder="templates/admin")


def init_app(app):
    db.init_app(app)

@DormDB_modify_blueprint.route("/admin/add_dorm", methods=['GET', 'POST'])
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

           
            new_dorm = dorms(name=name, state=state, city=city, sex=sex, price=price, meal_number=meal_number,
                             cleaning_plan=cleaning_plan, room_population=room_population, kitchen=kitchen,
                             laundry=laundry, park=park, wifi=wifi, studying_hall=studying_hall,
                             stars=stars, location=location, capacity=capacity, availability=availability,
                             latest_check_in=latest_check_in)

            db.session.add(new_dorm)
            db.session.commit()
            return render_template("admin/dorm_added.html", success=True, dorm=new_dorm)
        except Exception as e:
            flash('Failed to add dorm: ' + str(e), 'danger')
            return render_template("admin/dorm_added.html", success=False, error=str(e))

    with open('./data/state_and_cities.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template("admin/add_dorm.html", data=data)


@DormDB_modify_blueprint.route("/admin/modify_dorm", methods=['GET', 'POST'])
def admin_modify_dorm():
    dorm = None
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'search':
            dorm_name = request.form.get('dorm_name', '').strip()
            dorm = dorms.query.filter_by(name=dorm_name).first()
            if not dorm:
                flash('Dorm not found', 'error')

        elif action == 'update':
            dorm_id = request.form.get('dorm_id')
            dorm = dorms.query.get(dorm_id)
            if dorm:
                
                try:
                    availability = int(request.form.get('availability'))
                    price = int(request.form.get('price'))
                except ValueError:
                    flash('Invalid input types for availability or price', 'error')
                    return render_template('admin_modify_dorm.html', dorm=dorm)

                dorm.availability = availability
                dorm.price = price
                dorm.latest_update = db.func.current_timestamp() 
                db.session.commit()
                flash('Dorm updated successfully', 'success')
                return redirect(url_for('modify_dorm')) 
            else:
                flash('Dorm not found during update', 'error')

        elif action == 'delete':
            dorm_id = request.form.get('dorm_id')
            dorm = dorms.query.get(dorm_id)
            if dorm:
                db.session.delete(dorm)
                db.session.commit()
                flash('Dorm deleted successfully', 'success')
                return redirect(url_for('admin_modify_dorm')) 
            else:
                flash('Dorm not found during deletion', 'error')

    return render_template('admin/admin_modify_dorm.html', dorm=dorm)

