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
from models import db, User, Character, Planet, Favorite
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

# Route for getting all characters
@app.route('/people', methods=['GET'])
def get_people():
    # Query all characters from the database
    people = Character.query.all()
    # Serialize the data for each character and return it
    return jsonify([person.serialize() for person in people]), 200

# Route for getting a specific character by ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    # Query the specific character from the database
    person = Character.query.get(people_id)
    # If the character does not exist, return an error
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    # Serialize the data for the character and return it
    return jsonify(person.serialize()), 200

# Route for getting all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    # Query all planets from the database
    planets = Planet.query.all()
    # Serialize the data for each planet and return it
    return jsonify([planet.serialize() for planet in planets]), 200

# Route for getting a specific planet by ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    # Query the specific planet from the database
    planet = Planet.query.get(planet_id)
    # If the planet does not exist, return an error
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    # Serialize the data for the planet and return it
    return jsonify(planet.serialize()), 200

# Route for getting all users
@app.route('/users', methods=['GET'])
def get_users():
    # Query all users from the database
    users = User.query.all()
    # Serialize the data for each user and return it
    return jsonify([user.serialize() for user in users]), 200

# Route for getting all favorites of a user
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Get user_id from the query parameters
    user_id = request.args.get('user_id')
    # Query the specific user from the database
    user = User.query.get(user_id)
    # If the user does not exist, return an error
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    # Serialize the data for each favorite of the user and return it
    return jsonify([favorite.serialize() for favorite in user.favorites]), 200

# Route for adding a favorite planet for a user
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # Get user_id from the query parameters
    user_id = request.args.get('user_id')
    # Query the specific user from the database
    user = User.query.get(user_id)
    # If the user does not exist, return an error
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    # Query the specific planet from the database
    planet = Planet.query.get(planet_id)
    # If the planet does not exist, return an error
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    # Create a new favorite with the user and planet
    favorite = Favorite(user_id=user.id, planet_id=planet.id)
    # Add the new favorite to the database
    db.session.add(favorite)
    # Commit the changes to the database
    db.session.commit()
    # Return a success message
    return jsonify({"msg": "Planet added to favorites"}), 200

# Route for adding a favorite character for a user
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    # Get user_id from the query parameters
    user_id = request.args.get('user_id')
    # Query the specific user from the database
    user = User.query.get(user_id)
    # If the user does not exist, return an error
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    # Query the specific character from the database
    person = Character.query.get(people_id)
    # If the character does not exist, return an error
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    
    # Create a new favorite with the user and character
    favorite = Favorite(user_id=user.id, character_id=person.id)
    # Add the new favorite to the database
    db.session.add(favorite)
    # Commit the changes to the database
    db.session.commit()
    # Return a success message
    return jsonify({"msg": "Person added to favorites"}), 200

# Route for deleting a favorite planet for a user
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Get user_id from the query parameters
    user_id = request.args.get('user_id')
    # Query the favorite from the database
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    # If the favorite does not exist, return an error
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404
    # Delete the favorite from the database
    db.session.delete(favorite)
    # Commit the changes to the database
    db.session.commit()
    # Return a success message
    return jsonify({"msg": "Planet removed from favorites"}), 200

# Route for deleting a favorite character for a user
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    # Get user_id from the query parameters
    user_id = request.args.get('user_id')
    # Query the favorite from the database
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    # If the favorite does not exist, return an error
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404
    # Delete the favorite from the database
    db.session.delete(favorite)
    # Commit the changes to the database
    db.session.commit()
    # Return a success message
    return jsonify({"msg": "Person removed from favorites"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)