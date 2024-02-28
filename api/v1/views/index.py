#!/usr/bin/python3
"""
creates a route
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage_t

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """An end point that retrives number of object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats), 200