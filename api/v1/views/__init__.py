#!/usr/bin/python3
"""
Views
"""
from flask import Blueprint

<<<<<<< HEAD

"""Create a Blueprint instance with URL prefix /api/v1"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""of everything in the index.py module"""
from api.v1.views.index import *
"""from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
"""
=======
app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *
>>>>>>> master
