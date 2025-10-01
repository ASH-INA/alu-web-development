#!/usr/bin/env python3
""" Basic Flask app for user authentication service
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome route

    Returns:
        JSON welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register a new user

    Returns:
        JSON response indicating success or failure
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """User login route

    Returns:
        JSON response with login status and session cookie
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    # Validate login credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session for user
    session_id = AUTH.create_session(email)

    # Create response
    response = make_response(jsonify({
        "email": email,
        "message": "logged in"
    }))

    # Set session cookie
    response.set_cookie('session_id', session_id)
    
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """User logout route

    Returns:
        Redirect to home page or 403 error
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    # Find user by session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # Destroy the session
        AUTH.destroy_session(user.id)
        # Redirect to home page
        return redirect('/')
    else:
        # User not found
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
