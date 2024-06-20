from flask import Blueprint, render_template, request, redirect, session, url_for, flash,jsonify
import json
from user.models import User
from admin.dormDB import dorms as Dorm
from sqlalchemy import and_



detailed_search_blueprint = Blueprint("detailed_search",__name__,static_folder="static",template_folder="detailed_search")
DS_results_blueprint = Blueprint("DS_results",__name__,static_folder="static",template_folder="detailed_search")
DD_page_blueprint = Blueprint("DD_page",__name__,static_folder="static",template_folder="detailed_search")

@detailed_search_blueprint.route('/detailed_search', methods=['GET', 'POST'])
def detailed_search():
    if request.method == 'POST':
       
        sex = request.form.get('sex')
        state = request.form.get('state')
        cities = request.form.getlist('city')
        meal_number = request.form.get('meal_number')
        cleaning_plan = request.form.get('cleaning_plan')
        room_population = request.form.get('room_population')
        min_price = request.form.get('min_price', type=float)
        max_price = request.form.get('max_price',type=float)
        stars = request.form.get('stars',type=float)
        amenities = request.form.getlist('amenities[]')
        latest_check_in = request.form.get('latest_check_in',type=int)  
        
        
        query = Dorm.query

       
        if sex != "":
            query = query.filter(Dorm.sex == sex)
            
        if state != "":
            query = query.filter(Dorm.state == state)
        
        if cities != [] and cities != [""]:
            query = query.filter(Dorm.city.in_(cities))
        
        if meal_number != "":
            query = query.filter(Dorm.meal_number == meal_number)
        
        if cleaning_plan != "":
            query = query.filter(Dorm.cleaning_plan == cleaning_plan)
        
        if room_population is not None:
            query = query.filter(Dorm.room_population <= room_population)
        
        if min_price is not None:
            query = query.filter(Dorm.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Dorm.price <= max_price)

        if stars is not None:
            query = query.filter(Dorm.stars >= stars)
        if latest_check_in is not None:
            query = query.filter(Dorm.latest_check_in >= latest_check_in)

        
        
        if amenities: 
            amenity_conditions = []
            if 'kitchen' in amenities:
                amenity_conditions.append(Dorm.kitchen == True)
            if 'laundry' in amenities:
                amenity_conditions.append(Dorm.laundry == True)
            if 'park' in amenities:
                amenity_conditions.append(Dorm.park == True)
            if 'wifi' in amenities:
                amenity_conditions.append(Dorm.wifi == True)
            if 'studying_hall' in amenities:
                amenity_conditions.append(Dorm.studying_hall == True)
            
            
            if amenity_conditions:
                query = query.filter(and_(*amenity_conditions))

        results = query.all()

        results_json = json.dumps([{
        'id' : result.dorm_id ,
        'owner_id':result.owner_id,
        'name': result.name,
        'state': result.state,
        'city': result.city,
        'meal_number': result.meal_number,
        'cleaning_plan': result.cleaning_plan,
        'room_population': result.room_population,
        'price': result.price,
        'kitchen': result.kitchen,
        'laundry': result.laundry,
        'studying_hall': result.studying_hall,
        'park': result.park,
        'wifi': result.wifi,
        'sex': result.sex,
        'stars': result.stars,
        'location': result.location,
        'capacity': result.capacity,
        'availability': result.availability,
        'latest_check_in': result.latest_check_in,
        'latest_update': result.latest_update.strftime('%Y-%m-%d') if result.latest_update else None
        } for result in results])
        return redirect(url_for('DS_results.results', results=results_json))
    
    with open('./data/state_and_cities.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template('detailed_search/detailed_searchUI.html', data=data)
 
@DS_results_blueprint.route('/detailed_search/results')
def results():
    results_json = request.args.get('results')
    results = json.loads(results_json)
    
    return render_template('detailed_search/results.html', results=results)

from flask_login import LoginManager, login_required, current_user

login_manager = LoginManager(DD_page_blueprint)
login_manager.login_view = 'user.login'   

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@DD_page_blueprint.route('/dormitory/<int:dorm_id>/<int:owner_id>')
def dormitory_detail(dorm_id,owner_id):
    dorm = Dorm.query.get_or_404(dorm_id)
    session['dorm_id'] = dorm_id
    session['owner_id'] = owner_id
    return render_template('detailed_search/dorm_detail.html', dorm=dorm,current_user=current_user)

