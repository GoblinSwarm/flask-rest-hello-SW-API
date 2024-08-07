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
import requests

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

@app.route('/favorite', methods=['GET'])
def handle_get_favorites():
    favorites = Favorite()
    favorites = favorites.query.all()
    return jsonify([item.serialize() for item in favorites]), 200

@app.route('/users/<int:theid>', methods=['GET'])
def handle_get_one_user(theid=None):
    if theid is not None:
        user = User()
        user = user.query.get(theid)
        if user is not None:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({"message": "User not found"}), 404

@app.route('/people/<int:theid>', methods=['GET'])
def handle_get_one_character(theid=None):
    if theid is not None:
        character = Character()
        character = character.query.get(theid)
        if character is not None:
            return jsonify(character.serialize()), 200
        else:
            return jsonify({"message": "Character not found"}), 404

@app.route('/planets/<int:theid>', methods=['GET'])
def handle_get_one_planet(theid=None):
    if theid is not None:
        planet = Planet()
        planet = planet.query.get(theid)
        if planet is not None:
            return jsonify(planet.serialize()), 200
        else: 
            return jsonify({"message": "Planet not found"}), 404

@app.route("/favorite/planet/<int:theid>", methods=["DELETE"])
def delete_planet_from_favorite(theid=None):
    
    favorite = Favorite()
    favorite = favorite.query.all()

    for fav in favorite:
        if fav['nature'] == 'PLANET':
            if fav['planet_id'] == theid:
                db.session.delete(fav)
                db.session.commit()
                return jsonify({"message": "Favorito borrado correctamente"}), 200
    
    return jsonify({"message": "Favorito ya esta borrado"}), 404

@app.route("/favorite/people/<int:theid>", methods=["DELETE"])
def delete_people_from_favorite(theid=None):
    
    favorite = Favorite()
    favorite = favorite.query.all()

    for fav in favorite:
        if fav['nature'] == 'CHARACTER':
            if fav['character_id'] == theid:
                db.session.delete(fav)
                db.session.commit()
                return jsonify({"message": "Favorito borrado correctamente"}), 200
    
    return jsonify({"message": "Favorito ya esta borrado"}), 404

@app.route("/favorite/planet/<int:theid>", methods=['POST'])
def handle_add_planet_to_favorite(planet_id=None):
    #This id is fictional as the id will be brought by the body
    user_id = 1;

    favorite = Favorite()
    favorite.user_id = user_id
    favorite.planet_id = planet_id

    db.session.add(favorite)

    try:
        db.session.commit()
        return jsonify("Se guardo planeta exitosamente") , 201
    except Exception as error:
        db.session.rollback
        return jsonify({"message": "Planet couldnt be saved"}), 400

@app.route("/favorite/people/<int:theid>", methods=['POST'])
def handle_add_character_to_favorite(character_id=None):
    #This id is fictional as the id will be brought by the body
    user_id = 1;

    favorite = Favorite()
    favorite.user_id = user_id
    favorite.character_id = character_id

    db.session.add(favorite)

    try:
        db.session.commit()
        return jsonify("Se guardo personaje exitosamente") , 201
    except Exception as error:
        db.session.rollback
        return jsonify({"message": "Personaje couldnt be saved"}), 400

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json

    required_fields = ['email', 'fullname', 'username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    user = User(email=data['email'],
                fullname=data['fullname'],
                username=data['username'],
                password=data['password'])
    #email, firstname, lastname, username
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "I am here mf"})

#Population starts here
@app.route("/people/populate", methods=['GET'])
def get_people_population():
    #https://www.swapi.tech/api/people?page=1&limit=2
    response = requests.get("https://www.swapi.tech/api/people?page=1&limit=300")
    response = response.json()
    response = response.get("results")

    for item in response:
        result = requests.get(item.get("url"))
        result = result.json()
        result = result.get("result")
        people = Character()
        people.name = result.get("properties").get("name")
        people.height = result.get("properties").get("height")
        people.mass = result.get("properties").get("mass")
        people.hair_color = result.get("properties").get("hair_color")
        people.skin_color = result.get("properties").get("skin_color")
        people.eye_color = result.get("properties").get("eye_color")
        people.birth_year = result.get("properties").get("birth_year")
        people.gender = result.get("properties").get("hair_color")
        db.session.add(people)

    try:
        db.session.commit()
        return jsonify("Adding Characters to DB"), 200
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify("error"), 500

@app.route("/planet/populate", methods=['GET'])
def get_planet_population():
    response = requests.get("https://www.swapi.tech/api/planets?page=1&limit=300")
    response = response.json()
    response = response.get("results")

    for item in response:
        result = requests.get(item.get("properties").get('url'))
        result = result.json()
        result = result.get("result")
        planet = Planet()
        planet.name = result.get("properties").get("name")
        planet.diameter = result.get("properties").get("diameter")
        planet.rotation_period = result.get("properties").get("rotation_period")
        planet.orbital_period = result.get("properties").get("orbital_period")
        planet.gravity = result.get("properties").get("gravity")
        planet.population = result.get("properties").get("population")
        planet.climate = result.get("properties").get("climate")
        planet.terrain = result.get("properties").get("terrain")
        planet.surface_water = result.get("properties").get("surface_water")
        db.session.add(planet)

    try:
        db.session.commit()
        return jsonify("Adding Planet to DB"), 200
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify("error"), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
