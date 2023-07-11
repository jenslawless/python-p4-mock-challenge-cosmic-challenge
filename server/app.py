#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Scientists(Resource):

    def get(self):
        scientists = Scientist.query.all()
        scientists_serialized = []
        for sci in scientists:
            sci_dict = {
                "id": sci.id,
                "name": sci.name,
                "field_of_study": sci.field_of_study,
            }
            scientists_serialized.append(sci_dict)
            
        response = make_response(
            jsonify(scientists_serialized),
            200
        )

        return response
    
    def post(self):

        data = request.get_json()

        new_sci = Scientist(
            name=data['name'],
            field_of_study=data['field_of_study'],
        )

        db.session.add(new_sci)
        db.session.commit()

        return make_response(new_sci.to_dict(), 201)

class IndiScientists(Resource):

    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if scientist:
            return make_response(scientist.to_dict(), 200)
        else: 
           return make_response({"error": "Scientist not found"}) 
        
    
    def patch(self, id):
        data = request.get_json()

        scientist = Scientist.query.filter_by(id=id).first()
        for attr in data:
            setattr(scientist, attr, data[attr])
        
        db.session.add(scientist)
        db.session.commit()

        response = make_response(
            jsonify(scientist.to_dict()),
            202
        )

        return response 
    
    def delete(self, id):

        scientist = Scientist.query.filter_by(id=id).first()
        db.session.delete(scientist)
        db.session.commit()

        return make_response('', 204)

class Planets(Resource):

    def get(self):
        planets = Planet.query.all()
        planets_serialized = []
        for pla in planets:
            pla_dict = {
                "id": pla.id,
                "name": pla.name,
                "distance_from_earth": pla.distance_from_earth,
                "nearest_star": pla.nearest_star,
            }
            planets_serialized.append(pla_dict)
            
        response = make_response(
            jsonify(planets_serialized),
            200
        )

        return response

class Missions(Resource):

    def post(self):
        data = request.get_json()

        new_mission = Mission(
            name=data['name'],
            scientist_id=data['scientist_id'],
            planet_id=data['planet_id'],
        )

        db.session.add(new_mission)
        db.session.commit()

        return make_response(new_mission.to_dict(), 201)


api.add_resource(Missions,  '/missions')   
api.add_resource(Planets, '/planets')
api.add_resource(Scientists, '/scientists')
api.add_resource(IndiScientists, '/scientists/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
