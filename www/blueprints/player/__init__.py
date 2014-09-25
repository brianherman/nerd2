from flask import Blueprint, render_template, send_file
from StringIO import StringIO
from models.cache import Cache
from models.playertime import PlayerTime

import re
import json
import requests

blueprint = Blueprint('player', __name__, template_folder='templates')

@blueprint.route('/p/<username>/')
def player(username):
    m = re.match('^[0-9A-Za-z_]{1,16}$', username)
    if m:
        online = {}
        for server in ['creative', 'pve']:
            players = json.loads(Cache.query.filter_by(key='MC_%s_ONLINE' % server.upper()).first().value)
            if username in players:
                online[server] = True
            else:
                online[server] = False
        playertime = PlayerTime.query.filter_by(playername=username).all()
        options = {
            'title': username,
            'username': username,
            'online': online,
            'playertime': playertime,
        }
        return render_template('player.html', **options)
    else:
        abort(404)

@blueprint.route('/p/<username>/skin.png')
def skin(username):
    r = requests.get('http://s3.amazonaws.com/MinecraftSkins/%s.png' % username)
    if r.status_code == 200:
        return send_file(StringIO(r.content), mimetype='image/png')
    else:
        return send_file('data/char.png', mimetype='image/png')
