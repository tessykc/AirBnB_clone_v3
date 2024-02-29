#!/usr/bin/python
""" holds class Amenity"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)


    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance.
        Create the initial dictionary using BaseModel's to_dict method"""
        base_dict = super().to_dict()
        """Add Amenity specific key/values"""
        base_dict['__class__'] = type(self).__name__
        return base_dict
