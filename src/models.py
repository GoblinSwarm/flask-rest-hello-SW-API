from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum

db = SQLAlchemy()

class Nature(PyEnum):
    PLANET = 'planet'
    CHARACTER = 'character'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    url = db.Column(db.String(250))
    orbital_period = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    climate = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "climate": self.climate
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250))
    birth_year = db.Column(db.String(20), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def __repr__(self):
        return '<Character %r>' % self.fullname
    
    def serialize(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "height": self.height,
            "weight": self.weight,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nature = db.Column(db.Enum(Nature), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True, unique=True)  
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True, unique=True)
    # Relationships
    user = db.relationship(User)
    planet = db.relationship(Planet, uselist=False) 
    character = db.relationship(Character, uselist=False)



#Right now i dont need the diagram, but its interesting in a certain way to have it here

# try:
#     render_er(Base, 'diagram.png')
#     print("Success! Check the diagram.png file")
# except Exception as e:
#     print("There was a problem generating the diagram")
#     raise e