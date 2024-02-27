#!/usr/bin/python3
"""
Route for handling places and amenities linking.
"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage
from models.place import Place
from models.amenity import Amenity


#@app_views.route("/places/<place_id>/amenities",
#                 methods=["GET"],
#                 strict_slashes=False)
#def amenity_by_place(place_id):
#  """
#  Get all amenities of place
#  :param place_id: Amenity id
#  :return: All amenities
#  """
#  fetched_obj = storage.get("Place", str(place_id))

#  all_amenities = []

#  if fetched_obj is None:
#    abort(404)

#  for obj in fetched_obj.amenities:
#    all_amenities.append(obj.to_json())

#  return jsonify(all_amenities)


#@app_views.route("places/<place_id>/amenities",
#                 methods=["DELETE"],
#                 strict_slashes=False)
#def unlink_amenity_from_place(place_id, amenity_id):
#  """
#  unlink an amenity in place
#  :param place_id: place id
#  :param amenity_id: amenity id
#  :return: empty dict or error
#  """
#  if not storage.get("Place", str(place_id)):
#    abort(404)
#  if not storage.get("Amenity", str(amenity_id)):
#    abort(404)

#  fetched_obj = storage.get("Place", (place_id)
#  found = 0

#  for obj in fetched_obj.amenities:
#    if str(obj.id) == obj.amenity_id:
#      if getenv("HBNB_TYPE_STORAGE") == "db":
#        fetched_obj.amenities.remove(obj)
#      else:
#        fetched_obj.amenity_ids.remove(obj)
#      fetched_obj.save()
#      found = 1
#      break

#  if found == 0:
#    abort(404)
#  else:
#    resp = jsonify({})
#    resp.status_code = 201
#    return resp


#@app_views.route("places/<place_id>/amenities",
#                 methods=["POST"],
#                 strict_slashes=False)
#def link_amenity_to_place(place_id, amenity_id):
#  """
#  link an amenity in place
#  :param place_id: place id
#  :param amenity_id: amenity id
#  :return: returns amenity obj added or error
#  """

#  fetched_obj = storage.get("Place", str(place_id))
#  amenity_obj = storage.get("Amenity", str(amenity_id))
#  found_amenity = None

#  if not fetched_obj or not amenity_obj:
#    abort(404)

#  for obj in fetched_obj.amenities:
#    if str(obj.id) == amenity_id:
#      found_amenity = obj
#      break

#  if found_amenity is not None:
#    return jsonify(found_amenity.to_json())

#  if getenv("HBNB_TYPE_STORAGE") == "db":
#    fetched_obj.amenities.append(amenity_obj)
#  else:
#    fetched_obj.amenities = amenity_obj

#  fetched_obj.save()

#  resp = jsonify(amenity_obj.to_json())
#  resp.status_code = 201

#  return resp

@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def amenity_by_place(place_id):
    """Get all amenities of a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    
    amenities = [amenity.to_json() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """Unlink an amenity from a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_json()), 200

    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_json()), 201