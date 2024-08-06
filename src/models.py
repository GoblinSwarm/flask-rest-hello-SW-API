from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from enum import Enum as PyEnum

db = SQLAlchemy()

class Nature(PyEnum):
    PLANET = 'planet'
    CHARACTER = 'character'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    favorite = db.relationship('Favorite', backref='user', uselist=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
        }
    
    def serialize_fav(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            # do not serialize the password, its a security breach
            "favorites": list(map(lambda item: item.serialize(), self.favorite))
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(120), nullable=False)
    orbital_period = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "population": self.population,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250))
    birth_year = db.Column(db.String(20), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Character %r>' % self.fullname
    
    def serialize(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "created_at": self.created_at
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)  
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    # Relationships

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }


#Right now i dont need the diagram, but its interesting in a certain way to have it here

# try:
#     render_er(Base, 'diagram.png')
#     print("Success! Check the diagram.png file")
# except Exception as e:
#     print("There was a problem generating the diagram")
#     raise e