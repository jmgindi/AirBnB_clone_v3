#!/usr/bin/python3
""" Cities view for HBNB API """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
import json


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def review_list(place_id):
    """ GET: render a list of reviews
        POST: Create a review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "POST":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        if "text" not in request.json:
            return jsonify({"error": "Missing text"}), 400
        if "user_id" not in request.json:
            return jsonify({"error": "Missing user_id"}), 400
        if not storage.get(User, new_dict["user_id"]):
            abort(404)
        new_dict["place_id"] = place_id
        review = Review(**new_dict)
        storage.new(review)
        storage.save()
        storage.close()
        return jsonify(place.to_dict()), 201
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def review_detail(review_id):
    """ GET: Return a json of a review detail
        DELETE: Deltes an object and returns an empty json dictionary
        PUT: Updates a review
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        storage.close()
        return jsonify({}), 200
    elif request.method == "PUT":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in new_dict.items():
            if k not in ["id",
                         "user_id",
                         "place_id",
                         "created_at",
                         "updated_at"]:
                setattr(review, k, v)
        storage.new(review)
        storage.save()
        storage.close()
    return jsonify(review.to_dict())
