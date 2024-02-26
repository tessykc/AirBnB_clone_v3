#!/usr/bin/python3

"""
Returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify


"""Define a route /status on the app_views Blueprint"""
@app_views.route('/status')
def status():
    """A route that returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    function to return the count of all class objects
    """
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)