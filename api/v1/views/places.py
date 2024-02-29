#!/usr/bin/python3
"""
Place objects that handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, City, User, Place, State, Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    search_criteria = request.get_json()
    if not search_criteria or all(len(v) == 0 for
                                  v in search_criteria.values()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = search_criteria.get('states', [])
    cities = search_criteria.get('cities', [])
    amenities = search_criteria.get('amenities', [])

    if not isinstance(states, list) or not isinstance(cities,
                                                      list) or not isinstance(
                                                          amenities, list):
        return jsonify({"error": "Invalid search criteria"}), 400

    matching_places = []
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                matching_places.extend(state.places)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                matching_places.extend(city.places)

    if not states and not cities:
        places = storage.all(Place).values()
        matching_places.extend(places)

    if amenities:
        amenities_objs = [storage.get(Amenity, amenity_id)
                          for amenity_id in amenities]
        matching_places = [place for place in matching_places
                           if all(amenity in place.amenities for
                                  amenity in amenities_objs)]

    return jsonify([place.to_dict() for place in matching_places])
