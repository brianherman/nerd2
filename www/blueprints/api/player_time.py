from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.playertime import PlayerTime

import json


class UpdatePlayerTimes(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("json", type=str, required=True)
    def post(self):
        args = self.post_parser.parse_args()

        stats = json.loads(args.get("json"))
        for stat in stats:
            playertime = PlayerTime.query.filter_by(
                playername=stat['playername'],
                server=stat['server']
            ).first()
            if playertime:
                playertime.seconds = stat['seconds']
            else:
                playertime = PlayerTime(
                    stat['playername'],
                    stat['server'],
                    stat['seconds']
                )
                db.session.add(playertime)
        db.session.commit()

        return {'success': True}


api.add_resource(UpdatePlayerTimes, '/update_player_times')
