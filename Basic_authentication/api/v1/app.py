#!/usr/bin/env python3
"""
Route module for the API

This is the main application module that configures and runs the Flask API.
It sets up CORS, registers blueprints, and defines
error handlers for the application.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


# Create Flask application instance
app = Flask(__name__)

# Register the blueprint containing all API routes
app.register_blueprint(app_views)

# Configure CORS (Cross-Origin Resource Sharing)
# Allows requests from any origin to API routes under /api/v1/*
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> str:
    """
    404 Not Found Error Handler

    Handles all 404 errors that occur when a route is not found.

    Args:
        error: The error object passed by Flask

    Returns:
        JSON: A JSON error response with 404 status code

    Example Response:
        {
            "error": "Not found"
        }
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    401 Unauthorized Error Handler

    Handles all 401 Unauthorized errors that occur when
    authentication is required
    but not provided or invalid.

    Args:
        error: The error object passed by Flask

    Returns:
        JSON: A JSON error response with 401 status code

    Example Response:
        {
            "error": "Unauthorized"
        }
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    """
    Main execution block - runs the Flask development server.

    The server host and port can be configured through environment variables:
    - API_HOST: Host address (default: "0.0.0.0")
    - API_PORT: Port number (default: "5000")
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
