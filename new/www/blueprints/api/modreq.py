from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.modreq import Modreq


class UpdateModreq(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("id", type=int, required=True)
    post_parser.add_argument("server", type=str, required=True)
    post_parser.add_argument("status", type=str, required=True)
    post_parser.add_argument("request_by", type=str, required=True)
    post_parser.add_argument("response_by", type=str, required=True)
    post_parser.add_argument("request_text", type=str, required=True)
    post_parser.add_argument("response_text", type=str, required=True)

    def post(self):
        args = self.post_parser.parse_args()

        modreq = Modreq.query.filter_by(
            id=args.get("id"),
            server=args.get("server")
        ).first()
        if not modreq:
            modreq = Modreq(
                args.get("id"),
                args.get("server"),
                args.get("status"),
                args.get("request_by"),
                args.get("response_by"),
                args.get("request_text"),
                args.get("response_text")
            )
            db.session.add(modreq)
        db.session.commit()

        return {
            'id': args.get("id"),
            'server': args.get("server"),
            'status': args.get("status"),
            'request_by': args.get("request_by"),
            'response_by': args.get("response_by"),
            'request_text': args.get("request_text"),
            'response_text': args.get("response_text")
        }

api.add_resource(UpdateModreq, '/update_modreq')

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
