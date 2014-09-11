from flask import app
from flask.ext.restful import Api

api = Api(prefix='/api')

from . import cache, creation
