#!/usr/bin/env python3
""" 
Module of Index views

This module contains the blueprint routes for the API index endpoints.
It handles status checks, statistics, and error testing endpoints.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ 
    GET /api/v1/status

    Endpoint to check the API status and ensure it's running properly.

    Returns:
        JSON: A JSON object containing the status of the API

    Example Response:
        {
            "status": "OK"
        }
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ 
    GET /api/v1/stats

    Endpoint to retrieve statistics about the objects in the database.
    Currently returns the count of User objects.

    Returns:
        JSON: A JSON object containing statistics

    Example Response:
        {
            "users": 42
        }
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized

    Testing endpoint that intentionally raises a 401 Unauthorized error.
    This endpoint is used to test the 401 error handler.

    Raises:
        401: Unauthorized error using Flask's abort function

    Note:
        This endpoint will always return a 401 error and is meant for testing purposes only.
    """
    abort(401)
