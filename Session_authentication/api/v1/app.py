#!/usr/bin/env python3
""" Flask app module """
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os

from api.v1.views import app_views
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth variable
auth = None

# Load authentication instance based on AUTH_TYPE
auth_type = os.getenv('AUTH_TYPE')

if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'auth':
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Filter each request before processing"""
    if auth is None:
        return

    # Paths that don't require authentication
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    # Check if current path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Check if both authorization header and session cookie are None
    auth_header = auth.authorization_header(request)
    session_cookie = auth.session_cookie(request)

    if auth_header is None and session_cookie is None:
        abort(401)

    # Get current user and assign to request
    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)

    # Assign current_user to request object
    request.current_user = current_user


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
