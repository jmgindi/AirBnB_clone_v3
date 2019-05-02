#!/usr/bin/python3
""" View for User objects """
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"],
                 strict_slashes=False)
def user_list():
    """ GET: Render a list of users
        POST: creates a new user
    """
    if request.method == "POST":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        if "email" not in new_dict:
            return jsonify({"error": "Missing email"}), 400
        if "password" not in new_dict:
            return jsonify({"error": "Missing password"}), 400
        new_user = User(**new_dict)
        storage.new(new_user)
        storage.save()
        storage.close()
        return jsonify(new_user.to_dict()), 201
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def detail_user(user_id):
    """ Work on a specific user with GET PUT DELETE methods """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        storage.close()
        return jsonify({})
    if request.method == "PUT":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in new_dict.items():
            if k not in ["id", "updated_at", "created_at"]:
                setattr(user, k, v)
        user.save()
    return jsonify(user.to_dict())
