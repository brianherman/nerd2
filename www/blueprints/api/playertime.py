from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.playertime import PlayerTime

class UpdatePlayerTime(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("playername", required=True)
    post_parser.add_argument("server", type=str, required=True)
    post_parser.add_argument("seconds", type=int, required=True)
    def post(self):
        args = self.post_parser.parse_args()

        playertime = PlayerTime.query.filter_by(
            playername=args.get("playertime"),
            server=args.get("server"),
            seconds=args.get("seconds")
        ).first()
        if playertime:
            playertime.seconds = args.get("seconds")
        else:
            playertime = PlayerTime(
                args.get("playername"),
                args.get("server"),
                args.get("seconds")
            )
            db.session.add(playertime)
        db.session.commit()

        return {
            'playername': args.get("playername"),
            'server': args.get("server"),
            'seconds': args.get("seconds")
        }

api.add_resource(UpdatePlayerTime, '/update_playertime')
