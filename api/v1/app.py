#!/usr/bin/python3
"""
Flask app for AirBnB
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)


"""Enable CORS for all routes"""
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


# Define a handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
