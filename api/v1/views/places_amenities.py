#!/usr/bin/python3
"""
Route for handling places and amenities linking.
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage

