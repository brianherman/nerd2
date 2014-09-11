from flask import render_template
from models.cache import Cache

def init_app(application):

    @application.context_processor
    def inject_servers():
        server_names = ['creative', 'survival', 'pve']
        return dict(server_names=server_names)


    @application.context_processor
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

    @application.errorhandler(404)
    @application.errorhandler(500)
    def error(error):
        options = {
            'title': 'Oh no! %s' % error.message,
            'error': error,
        }
        return render_template('error.html', **options), error.code
