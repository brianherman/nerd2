from www.app import app
from flask.ext.restful import Api

api = Api(app, '/api')

from . import cache, creation
