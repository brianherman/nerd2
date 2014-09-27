from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.modreq import Modreq

import json


class UpdateModreqs(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("json", type=str, required=True)

    def post(self):
        args = self.post_parser.parse_args()

        modreqs = json.loads(args.get("json"))
        for modreq in modreqs:
            modreq_obj = Modreq.query.filter_by(
                id=modreq['id'],
                server=modreq['server']
            ).first()
            if modreq_obj:
                modreq_obj.status = modreq['status']
                modreq_obj.response_by = modreq['response_by']
                modreq_obj.response_text = modreq['response_text']
            else:
                modreq_obj = Modreq(
                    modreq['id'],
                    modreq['server'],
                    modreq['status'],
                    modreq['request_by'],
                    modreq['response_by'],
                    modreq['request_text'],
                    modreq['response_text']
                )
                db.session.add(modreq_obj)
        db.session.commit()

        return {'success': True}


api.add_resource(UpdateModreqs, '/update_modreqs')


class GetModreqs(Resource):
    get_parser = RequestParser()
    get_parser.add_argument("server", type=int, required=True)
    def get(self):
        args = self.get_parser.parse_args()

        creations = Modreq.query.filter_by(server=args.get("server"))
        response = []

        for modreq in creations:
            response.append(dict(
                id=modreq.id,
                server=modreq.server,
                status=modreq.status,
                request_by=modreq.request_by,
                response_by=modreq.response_by,
                request_text=modreq.request_text,
                response_text=modreq.response_text
            ))

        return response


api.add_resource(GetModreqs, '/get_modreqs')
