#!/usr/bin/python3
<<<<<<< HEAD
"""app.py to connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
=======
"""
A variable app
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage
>>>>>>> master


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

<<<<<<< HEAD

@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
=======
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    """
    Teardown functions
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 errors
    :return: Returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

    if __name__ == "__main__":
        app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
>>>>>>> master
