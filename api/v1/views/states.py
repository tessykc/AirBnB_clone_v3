#!/usr/bin/python3
"""
Route for handling state objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrives all state objects
    :return: json all states
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_dict())  # Changed to to_dict() from to_json()

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Create state route
    :return: newly created state obj
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)  # Fixed typo here
    new_state.save()
    resp = jsonify(new_state.to_dict())  # Changed to to_dict() from to_json()
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Get a specific state object by ID
    :param state_id: state object id
    :return: state object with the specified id or error
    """

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())  # Changed to to_dict() from to_json()


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Updates specific state object by id
    :param state_id: state object id
    :return: state obj and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)  # Fixed typo here
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())  # Changed to to_dict() from to_json()


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Deletes state by ID
    :param state_id: state obj id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
