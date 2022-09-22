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
from models import db, User, People, Planets, FavPeople, FavPlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route("/user", methods=["GET"])
def getUser():
    all_user = User.query.all()
    serializados = list( map(lambda user: user.serialize(), all_user))
    print(all_user)
    return jsonify({
        "mensaje": "Todos los usuarios",
        "user": serializados
    }), 200

@app.route("/people", methods=["GET"])
def getPeople():
    all_people = People.query.all()
    serializados = list( map(lambda people: people.serialize(), all_people))
    print(all_people)
    return jsonify({
        "mensaje": "Todos los personajes",
        "people": serializados
    }), 200

@app.route("/people/<int:idPersona>", methods=["GET"])
def getPeopleid(idPersona):
    one = People.query.filter_by(uid=idPersona).first()
    if(one):
        return jsonify({
        "id": idPersona,
        "people": one.serialize()
    }), 200
    else:
        return jsonify({
        "id": idPersona,
        "mensaje": "not found"
    }), 404   

@app.route("/planets", methods=["GET"])
def getPlanets():
    all_planets = Planets.query.all()
    serializados = list( map(lambda planets: planets.serialize(), all_planets))
    print(all_planets)
    return jsonify({
        "mensaje": "Todos los planetas",
        "planets": serializados
    }), 200

@app.route("/planets/<int:idPlanets>", methods=["GET"])
def getPlanetsid(idPlanets):
    one = Planets.query.filter_by(uid=idPlanets).first()
    if(one):
        return jsonify({
        "id": idPlanets,
        "planets": one.serialize()
    }), 200
    else:
        return jsonify({
        "id": idPlanets,
        "mensaje": "not found"
    }), 404   

@app.route("/user/favorites", methods=["GET"])
def getUserFav():
    return jsonify({
        "mensaje": "Lista de los favoritos del usuario",
        "userfav": []
    }), 200

@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def postPeopleFav(people_id):
    one = People.query.get(people_id)
    user = User.query.get(1)
    if(one):
        new_fav = FavPeople()
        new_fav.email = user.email
        new_fav.people_id = people_id
        db.session.add(new_fav)
        db.session.commit()
        return "Hecho!"
    else:
        raise APIException("no existe el personaje", status_code=404)

@app.route("/favorite/planets/<int:planets_id>", methods=['POST'])
def postPlanetsFav(planets_id):
    one = Planets.query.get(planets_id) #busqueda solo por el pk
    user = User.query.get(1)
    if(one):
        new_fav = FavPlanets()
        new_fav.email = user.email
        new_fav.planets_id = planets_id
        db.session.add(new_fav)
        db.session.commit()
        return "Hecho!"
    else:
        raise APIException("no existe el planeta", status_code=404)

@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def deletePeopleFav(people_id):
    one = FavPeople.query.filter_by(people=people_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return "eliminado"
    else:
        raise APIException("no existe el personaje", status_code=404)

@app.route("/favorite/planets/<int:planets_id>", methods=['DELETE'])
def deletePlanetsFav(planets_id):
    one = FavPlanets.query.filter_by(planets=planets_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return "eliminado"
    else:
        raise APIException("no existe el planeta", status_code=404)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
