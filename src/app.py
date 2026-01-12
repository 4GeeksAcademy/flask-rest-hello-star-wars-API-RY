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
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet


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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#Endpoints characters
@app.route('/people', methods=['GET'])
def get_all_people():
    characters = Character.query.all()
    return jsonify([c.serialize() for c in characters]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(person.serialize()), 200

#Endpoints planets 
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

#Endpoints users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Simulamos el usuario 1 para prueba
    user_id = 1 
    
    char_favs = FavoriteCharacter.query.filter_by(user_id=user_id).all()
    plan_favs = FavoritePlanet.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        "characters": [f.serialize() for f in char_favs],
        "planets": [f.serialize() for f in plan_favs]
    }), 200

# --- ENDPOINTS DE FAVORITOS (POST & DELETE) ---

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1 
    exists = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "Ya es favorito"}), 400
    
    new_fav = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planeta añadido a favoritos"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1
    exists = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if exists:
        return jsonify({"msg": "Ya es favorito"}), 400

    new_fav = FavoriteCharacter(user_id=user_id, character_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Personaje añadido a favoritos"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1
    fav = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
