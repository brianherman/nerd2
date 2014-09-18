from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.cache import Cache

class UpdateCache(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("key", type=str, required=True)
    post_parser.add_argument("value", required=True)
    def post(self):
        args = self.post_parser.parse_args()

        kv = Cache.query.filter_by(key=args.get("key")).first()
        if kv:
            kv.value = args.get("value")
        else:
            kv = Cache(args.get("key"), args.get("value"))
            db.session.add(kv)
        db.session.commit()

        return {'key': args.get("key"), 'value': args.get("value")}

api.add_resource(UpdateCache, '/update_cache')
