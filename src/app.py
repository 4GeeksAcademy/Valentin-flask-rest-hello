"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Address, Planet, Character, Vehicle, FavoriteList

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users=[user.serialize() for user in users])


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')
    phone_number = data.get('phone_number')
    email = data.get('email')
    inscription_date = data.get('inscription_date')

    new_user = User(username=username, password=password, name=name, surname=surname,
                    phone_number=phone_number, email=email, inscription_date=inscription_date)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message='User created successfully', user=new_user.serialize()), 201


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify(message='User not found'), 404


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.name = data.get('name', user.name)
    user.surname = data.get('surname', user.surname)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.email = data.get('email', user.email)
    user.inscription_date = data.get('inscription_date', user.inscription_date)

    db.session.commit()

    return jsonify(message='User updated successfully', user=user.serialize())


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message='User deleted successfully')
    else:
        return jsonify(message='User not found'), 404


@app.route('/addresses')
def get_addresses():
    addresses = Address.query.all()
    return jsonify(addresses=[address.serialize() for address in addresses])


@app.route('/planets')
def get_planets():
    planets = Planet.query.all()
    return jsonify(planets=[planet.serialize() for planet in planets])


@app.route('/characters')
def get_characters():
    characters = Character.query.all()
    return jsonify(characters=[character.serialize() for character in characters])


@app.route('/vehicles')
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify(vehicles=[vehicle.serialize() for vehicle in vehicles])


@app.route('/favorite-lists')
def get_favorite_lists():
    favorite_lists = FavoriteList.query.all()
    return jsonify(favorite_lists=[favorite_list.serialize() for favorite_list in favorite_lists])


@app.route('/favorite-lists', methods=['POST'])
def create_favorite_list():
    data = request.get_json()
    planet_id = data.get('planet_id')
    character_id = data.get('character_id')
    vehicle_id = data.get('vehicle_id')
    user_id = data.get('user_id')

    new_favorite_list = FavoriteList(planet_id=planet_id, character_id=character_id,
                                     vehicle_id=vehicle_id, user_id=user_id)
    db.session.add(new_favorite_list)
    db.session.commit()

    return jsonify(message='Favorite list created successfully', favorite_list=new_favorite_list.serialize()), 201


@app.route('/favorite-lists/<int:favorite_list_id>', methods=['DELETE'])
def delete_favorite_list(favorite_list_id):
    favorite_list = FavoriteList.query.get(favorite_list_id)
    if favorite_list:
        db.session.delete(favorite_list)
        db.session.commit()
        return jsonify(message='Favorite list deleted successfully')
    else:
        return jsonify(message='Favorite list not found'), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
