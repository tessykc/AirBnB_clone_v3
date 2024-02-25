#!/usr/bin/python3
"""
Route for handling places and amenities linking.
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
  """
  Get all amenities of place
  :param place_id: Amenity id
  :return: All amenities
  """
  fetched_obj = storage.get("Place", str(place_id))

  all-amenities = []

  if fetched_obj is None:
    abort(404)

  for obj in fetched_obj.amenities:
    all_amenities.append(obj.to_json())

  return jsonify(all_amenities)


@app_views.route("places/<place_id>/amenities",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
  """
