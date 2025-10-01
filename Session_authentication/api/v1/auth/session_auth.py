#!/usr/bin/env python3
""" Session Authentication views
"""
from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handle user login and create session"""
    # Get email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing or empty
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing or empty
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Check if password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth here to avoid circular imports
    from api.v1.app import auth

    # Create session for user
    session_id = auth.create_session(user.id)

    # Create response with user data
    response = make_response(user.to_json())

    # Set session cookie
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
