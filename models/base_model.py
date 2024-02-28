#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
import hashlib

time = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object

import models

class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, include_password=False, time="%Y-%m-%dT%H:%M:%S.%f"):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        
        new_dict["__class__"] = self.__class__.__name__
        
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
            return new_dict
        
        dict_representation = {}
        for key, value in self.__dict__.items():
            """Exclude private attributes and methods"""
            if not key.startswith('_') and not callable(value):
                dict_representation[key] = value
        
        if not include_password and 'password' in dict_representation:
            """Hash the password if it exists and is not included"""
            dict_representation['password'] = hashlib.md5(dict_representation['password'].encode()).hexdigest()
        return dict_representation

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
