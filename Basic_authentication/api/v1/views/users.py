#!/usr/bin/env python3
""" Module for User views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users() -> str:
    """GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    users = User.all()
    return jsonify([user.to_json() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str) -> str:
    """GET /api/v1/users/<user_id>
    Path parameter:
      - user_id
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    # Handle 'me' special case
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    # Original behavior for regular user IDs
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    try:
        user = User()
        user.email = data['email']
        user.password = data['password']
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        abort(400, "Can't create User: {}".format(str(e)))


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> str:
    """PUT /api/v1/users/<user_id>
    Path parameter:
      - user_id
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """DELETE /api/v1/users/<user_id>
    Path parameter:
      - user_id
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200
