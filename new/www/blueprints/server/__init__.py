from flask import Blueprint, request

from www.util import render_with_header

blueprint = Blueprint('server', __name__, template_folder='templates')

def _index(server):
    server = server.lower()
    if server not in ['creative', 'survival', 'pve']:
        abort(404)
    statuses = load_json('statuses.json')
    current_rev = load_json('current_rev.json')[server]


    options = {
        'title': server,
        'statuses': statuses,
        'addr': addr,
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
