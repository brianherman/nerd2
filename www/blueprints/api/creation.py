from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.creation import Creation

import json


class UpdateCreations(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("json", required=True)
    def post(self):
        args = self.post_parser.parse_args()

        creations = json.loads(args.get("json"))
        for creation in creations:
            creation_obj = Creation.query.filter_by(
                server=creation['server'],
                revision=creation['revision'],
                x=creation['x'],
                z=creation['z']
            ).first()
            if creation:
                pass
            else:
                creation_obj = Creation(
                    creation['name'],
                    creation['server'],
                    creation['revision'],
                    creation['x'],
                    creation['z']
                )
                db.session.add(creation_obj)
        db.session.commit()

        return {'success': True}


api.add_resource(UpdateCreations, '/update_creations')


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
