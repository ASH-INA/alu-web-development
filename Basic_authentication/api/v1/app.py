#!/usr/bin/env python3
"""
Flask app for Basic Authentication
"""
from flask import Flask, jsonify, abort
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Error handler for 401 Unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """Error handler for 404 Not Found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    import os
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
