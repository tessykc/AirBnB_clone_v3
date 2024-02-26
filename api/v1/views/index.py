#!/usr/bin/python3

"""
Returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, Blueprint, jsonify
from models import storage

stats_blueprint = Blueprint('stats', __name__, url_prefix='/api/v1')


"""Define a route /status on the app_views Blueprint"""
@app_views.route('/status', methods=['GET'])
def get_status():
    """A route that returns a JSON"""
    return jsonify({"status": "OK"})


@stats_blueprint.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve counts of each object type"""
    stats = {
        'amenities': storage.count('Amenities'),
        'cities': storage.count('Cities'),
        'places': storage.count('Places'),
        'reviews': storage.count('Reviews'),
        'states': storage.count('States'),
        'users' : storage.count('Users'),
    }
    return jsonify(stats)


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
      