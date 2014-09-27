from . import api
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from models import db
from models.player_time import PlayerTime

import json


class UpdatePlayerTimes(Resource):
    post_parser = RequestParser()
    post_parser.add_argument("json", type=str, required=True)
    def post(self):
        args = self.post_parser.parse_args()

        stats = json.loads(args.get("json"))
        for stat in stats:
            player_time = PlayerTime.query.filter_by(
                playername=stat['playername'],
                server=stat['server']
            ).first()
            if player_time:
                player_time.seconds = stat['seconds']
            else:
                player_time = PlayerTime(
                    stat['playername'],
                    stat['server'],
                    stat['seconds']
                )
                db.session.add(player_time)
        db.session.commit()

        return {'success': True}


api.add_resource(UpdatePlayerTimes, '/update_player_times')
