from flask import Blueprint, render_template, request, current_app
from www.models.cache import Cache

import json

def load_json(filename):
    with current_app.open_resource('scraped/'+filename) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d

def load_html(filename):
    with current_app.open_resource('scraped/'+filename) as html_data:
        d = html_data.read()
        html_data.close()
        return d

blueprint = Blueprint('server', __name__, template_folder='templates')

def _index(server):
    server = server.lower()
    if server not in ['creative', 'survival', 'pve']:
        abort(404)
    statuses = load_json('statuses.json')
    current_rev = int(Cache.query.filter_by(key='CURRENT_REVISION_'+server.upper()).first().value)

    options = {
        'title': server,
        'statuses': statuses,
        'addr': 'nerd.nu',#addr,
        'description': load_html('info-%s.html' % server),
        'status': statuses[server],
        'subreddit': load_json('subreddit.json')[server][:10],
        'github': filter(lambda a: server in a['tags'], load_json('github.json'))[:10],
        'current_rev': current_rev,
        'top_players': load_json('top_players.json')[server][:20]}

    if server == 'survival':
        del options['status']['players']
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
