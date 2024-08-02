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

@app.route('/user', methods=['GET'])
def handle_get_users():
    users = User()
    users = users.query.all()
    return jsonify([item.serialize() for item in users]), 200

@app.route('/people', methods=['GET'])
def handle_get_characters():
    characters = Character()
    characters = characters.query.all()
    return jsonify([item.serialize() for item in characters]), 200

@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planets = Planet()
    planets = planets.query.all()
    return jsonify([item.serialize() for item in planets]), 200

@app.route('/user/<int:theid>', methods=['GET'])
def handle_get_one_user(theid=None):
    if theid is not None:
        user = User()
        user = user.query.get(theid)
        if user is not None:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({"message": "User not found"}), 404

@app.route('/character/<int:theid>')
def handle_get_one_character(theid=None):
    if theid is not None:
        character = Character()
        character = character.query.get(theid)
        if character is not None:
            return jsonify(character.serialize()), 200
        else:
            return jsonify({"message": "Character not found"}), 404

@app.route('/planet/<int:theid>', methods=['GET'])
def handle_get_one_planet(theid=None):
    if theid is not None:
        planet = Planet()
        planet = planet.query.get(theid)
        if planet is not None:
            return jsonify(planet.serialize()), 200
        else: 
            return jsonify({"message": "Planet not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
