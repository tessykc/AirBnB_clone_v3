#!/usr/bin/python3

"""app.py to connect to API"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage
"""
A variable app
"""
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown_appcontext
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Teardown functions
    """
    data = [
        "error": returns 404 json
    }
    
    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

    if __name__ == "__main__":
        app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
