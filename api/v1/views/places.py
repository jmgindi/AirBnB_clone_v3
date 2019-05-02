#!/usr/bin/python3
""" Cities view for HBNB API """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
import json


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def places_city_get(city_id):
    """ GET: render a list of cities
        POST: Create a city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "POST":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in request.json:
            return jsonify({"error": "Missing name"}), 400
        if "user_id" not in request.json:
            return jsonify({"error": "Missing user_id"}), 400
        if new_dict["user_id"] not in storage.get("User", user_id):
            abort(404)
        new_dict["city_id"] = city_id
        place = Place(**new_dict)
        storage.new(place)
        storage.save()
        storage.close()
        return jsonify(place.to_dict()), 201
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def place_detail(place_id):
    """ GET: Return a json of a place detail
        DELETE: Deltes an object and returns an empty json dictionary
        PUT: Updates a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        storage.close()
        return jsonify({})
    elif request.method == "PUT":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in new_dict.items():
            if k not in ["id",
                         "user_id",
                         "city_id",
                         "created_at",
                         "updated_at"]:
                setattr(place, k, v)
        storage.new(place)
        storage.save()
        storage.close()
    return jsonify(place.to_dict())
