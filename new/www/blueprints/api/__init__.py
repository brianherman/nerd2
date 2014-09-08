from www.app import app
from flask.ext.restful import Api, Resource
from flask.ext.restful.reqparse import RequestParser
from www.models import db
from www.models.cache import Cache
from www.models.creation import Creation

api = Api(app, '/api')

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

class UpdateCreation(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("name", required=True)
    post_parser.add_argument("server", type=str, required=True)
    post_parser.add_argument("revision", type=int, required=True)
    post_parser.add_argument("x", type=int, required=True)
    post_parser.add_argument("z", type=int, required=True)
    def post(self):
        args = self.post_parser.parse_args()

        creation = Creation.query.filter_by(
            server=args.get("server"),
            revision=args.get("revision"),
            x=args.get("x"),
            z=args.get("z")
        ).first()
        if creation:
            pass
        else:
            creation = Creation(
                args.get("name"),
                args.get("server"),
                args.get("revision"),
                args.get("x"),
                args.get("z")
            )
            db.session.add(creation)
        db.session.commit()

        return {
            'name': args.get("name"),
            'server': args.get("server"),
            'revision': args.get("revision"),
            'x': args.get("x"),
            'z': args.get("z")
        }

api.add_resource(UpdateCreation, '/update_creation')

class GetCreations(Resource):
    get_parser = RequestParser()
    get_parser.add_argument("server", type=str, required=True)
    get_parser.add_argument("revision", type=int, required=True)
    def get(self):
        args = self.get_parser.parse_args()

        creations = Creation.query.filter_by(server=args.get("server"), revision=args.get("revision"))
        response = []

        for creation in creations:
            response.append(dict(
                name=creation.name,
                server=creation.server,
                revision=creation.revision,
                x=creation.x,
                z=creation.z
            ))

        return response

api.add_resource(GetCreations, '/get_creations')

# add_chat (server, data)
# add_player_event (server, player, event_type)
