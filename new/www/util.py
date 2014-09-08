from www.app import app
from www.models.cache import Cache

@app.context_processor
def inject_servers():
    server_names = ['creative', 'survival', 'pve']
    return dict(server_names=server_names)


@app.context_processor
def utility_processor():
    def get_status(server):
        return True
    def get_players(server):
        current = Cache.query.filter_by(
            key="MC_"+server.upper()+"_USERS_CURRENT"
        ).first().value
        max = Cache.query.filter_by(
            key="MC_"+server.upper()+"_USERS_MAX"
        ).first().value
        return current+'/'+max
    return dict(
        get_players=get_players,
        get_status=get_status)
