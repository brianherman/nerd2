from flask import Blueprint, render_template, request
from models.cache import Cache
from models.player_time import PlayerTime
import json

blueprint = Blueprint('server', __name__, template_folder='templates')

def _index(server):
    server = server.lower()
    if server not in ['creative', 'survival', 'pve']:
        abort(404)
    addr = {'creative': 'c.nerd.nu', 'survival': 's.nerd.nu', 'pve': 'p.nerd.nu'}
    current_rev = int(Cache.query.filter_by(key='CURRENT_REVISION_'+server.upper()).first().value)

    if server in ['creative', 'pve']:
        players = json.loads(Cache.query.filter_by(key='MC_%s_ONLINE' % server.upper()).first().value)
        top_players = PlayerTime.query.filter_by(server=server).order_by(PlayerTime.seconds.desc()).limit(10).all()
    else:
        players = None
        top_players = None

    options = {
        'title': server,
        'addr': addr,
        'players': players,
        'subreddit': json.loads(Cache.query.filter_by(key='REDDIT_POSTS').first().value),
        #'github': json.loads(Cache.query.filter_by(key='GITHUB_'+server.upper()+'_ISSUES').first().value),
        'current_rev': current_rev,
        'top_players': top_players
    }

    return render_template('server.html', **options)


@blueprint.route('/creative')
def creative_index():
    return _index('creative')

@blueprint.route('/survival')
def survival_index():
    return _index('survival')

@blueprint.route('/pve')
def pve_index():
    return _index('pve')
