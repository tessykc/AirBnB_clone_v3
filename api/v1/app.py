#!/usr/bin/python3

"""app.py to connect to API"""
import os
from models import storage
from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
"""
A variable app
"""
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown functions
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)