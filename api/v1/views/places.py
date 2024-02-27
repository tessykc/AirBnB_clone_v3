#!/usr/bin/python3
from flask import abort, jsonify, request
from models import storage, City, Place, User
from api.v1.views import app_views


def check_city(city_id):
    """Check if city_id is linked to any City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)


def check_place(place_id):
    """Check if place_id is linked to any Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)


def check_user(user_id):
    """Check if user_id is linked to any User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def handle_places(city_id):
    """Handle GET and POST requests for places."""
    if request.method == 'GET':
        check_city(city_id)
        city = storage.get(City, city_id)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    elif request.method == 'POST':
        check_city(city_id)
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        check_user(data['user_id'])
        if 'name' not in data:
            abort(400, 'Missing name')
        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_place(place_id):
    """Handle GET, DELETE, and PUT requests for a specific place."""
    check_place(place_id)
    place = storage.get(Place, place_id)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
