from V1.models import User, Ride, Request
from werkzeug.security import check_password_hash,generate_password_hash # pragma: no cover
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
from V1.auth import validate  # pragma: no cover
from flask_mail import Mail, Message 
from V1 import app # pragma: no cover
from flask import Blueprint,\
    jsonify, request, make_response  # pragma: no cover

ride_blueprint = Blueprint('ride', __name__)
users = []
logged_in_user = None

#Mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hcravens25@gmail.com'
app.config['MAIL_PASSWORD'] = 'ravens2018'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'hcravens25@gmail.com'
mail = Mail(app)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECS'] = ['access']
jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''Black listing'''
    jti = decrypted_token['jti']
    return jti in blacklist


@ride_blueprint.route('/api/v1/rides', methods=['POST'])
@jwt_required
def create_ride():
    '''Businesss registration route'''
    current_user = get_jwt_identity()
    data = request.get_json()
    category = data.get('category')
    pick_up = data.get('pick_up')
    drop_off = data.get('drop_off')
    date_time = data.get('date_time')
    price = data.get('price')
    dict_data = {'category' : category, 'pick_up':pick_up,
                 'drop_off':drop_off, 'date_time':date_time, 'price':price }
    if validate.val_none(**dict_data):
        result = validate.val_none(**dict_data)
        return jsonify(result), 406
    if validate.empty(**dict_data):
        result = validate.empty(**dict_data)
        return jsonify(result), 406
    njaro = Ride.ride.items()
    existing_ride = {k:v for k, v in njaro if data['category'] == v['category']}

    if existing_ride:
        return jsonify({"message":"Ride category already exists"})
    else:
        new_ride = Ride(category, pick_up, drop_off, date_time, price, current_user)
        new_ride.create_ride()
        response = {'message': 'Ride Successfully Created',
                    'Created by': current_user}
        return make_response(jsonify(response)), 201


@ride_blueprint.route('/api/v1/rides', methods=['GET'])
@jwt_required
def get_rides():
    '''route to get all rides'''
    # If GET method
    rides = Ride.get_all_rides()
    return make_response(jsonify(rides)), 200

@ride_blueprint.route('/api/v1/rides/<int:ride_id>', methods=['GET'])
def get_a_ride(ride_id):
    '''route to get a ride info'''
    target_ride = Ride.get_ride(ride_id)
    if target_ride:
        return make_response(jsonify(target_ride)), 200
    else:
        return jsonify(
            {'message': 'Resource Not Found'}), 404

@ride_blueprint.route('/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
@jwt_required
def create_request(ride_id):
    '''Route to post a ride request'''
    current_user = get_jwt_identity()
    if request.method == 'POST':
        requester = current_user
        new_request = Request(requester)
        new_request.add_request()
        response = {
            'message': 'Request Posted',
            'Request by': current_user
            }
        return make_response(jsonify(response)), 201

@ride_blueprint.route('/api/v1/rides/<int:ride_id>/requests', methods=['GET'])
def get_request(ride_id):
    '''Route to get a requets'''
    return make_response(jsonify(Request.get_all_requests())), 200