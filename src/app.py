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
from models import db, User, Characters, FavoriteCharacters, Planet, FavoritePlanet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

    # traer informacion de los usuarios


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({'msg': 'ok', 'user': users_serialized})


@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {id} no existe'}), 404
    return jsonify({'msg': 'ok', 'user': user.serialize()})

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    characters_serialized = []
    for characters in characters:
        characters_serialized.append(characters.serialize())
    print(characters_serialized)
    return jsonify({'msg': 'ok', 'character': characters_serialized})

@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    character = Characters.query.get(id)
    if character is None:
        return jsonify({'msg': f'El personaje con id {id} no existe'}), 404
    return jsonify({'msg': 'ok', 'character': character.serialize()})


@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'email' not in body:
        return jsonify({'msg': f'el campo \'email\' es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': f'el campo \'password\' es obligatorio'}), 400
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'ok', 'user': new_user.serialize()})

@app.route('/users/<int:user_id>/favorites', methods= ['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    favorite_characters_serialized = []      
    for favorite_characters in user.favorite_characters:
        print(favorite_characters.character) 
        favorite_characters_serialized.append(favorite_characters.character.serialize())

    favorite_planets_serialized = []      
    for favorite_planets in user.favorite_planets:
        print(favorite_planets.planet) 
        favorite_planets_serialized.append(favorite_planets.planet.serialize())
    
    return jsonify({'msg': 'ok', 'planet': favorite_planets_serialized, 'character': favorite_characters_serialized}), 200

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'El Planeta con id {planet_id} no existe'}), 404
    
    existing_favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify ({'msg': 'Este Planeta ya es un favorito'}), 409

    new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'msg': 'Planeta añadido a favoritos', 'favorite': new_favorite.serialize()}),201 

@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['POST'])
def create_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'El personaje con id {character_id} no existe'}), 404

    existing_favorite = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favorite:
        return jsonify({'msg': 'Este personaje ya está en favoritos'}), 409

    new_favorite = FavoriteCharacters(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'msg': 'Personaje añadido a favoritos', 'favorite': new_favorite.serialize()}), 201


@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'msg': 'El planeta no está en la lista de favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'msg': 'Planeta eliminado de favoritos'}), 200

@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    favorite = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({'msg': 'El personaje no está en la lista de favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'msg': 'Personaje eliminado de favoritos'}), 200

@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'El personaje con id {character_id} no existe'}), 404

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    if 'name' in body:
        character.name = body['name']
    if 'height' in body:
        character.height = body['height']
    if 'weight' in body:
        character.weight = body['weight']

    db.session.commit()

    return jsonify({'msg': 'Personaje actualizado correctamente', 'character': character.serialize()}), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'El planeta con id {planet_id} no existe'}), 404

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    if 'name' in body:
        planet.name = body['name']
    if 'population' in body:
        planet.population = body['population']
    if 'weather' in body:
        planet.weather = body['weather']

    db.session.commit()

    return jsonify({'msg': 'Planeta actualizado correctamente', 'planet': planet.serialize()}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
