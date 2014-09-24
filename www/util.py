from flask import render_template
from models.cache import Cache

def init_utils(application):

    @application.context_processor
    def inject_servers():
        server_names = ['creative', 'survival', 'pve']
        return dict(server_names=server_names)

    @application.context_processor
    def utility_processor():
        def get_status(server):
            status = Cache.query.filter_by(
                key="MC_%s_STATUS" % server.upper()
            ).first().value
            if status == 'offline':
                return False
            elif status == 'online':
                return True
        def get_players(server):
            current = Cache.query.filter_by(
                key="MC_%s_USERS_CURRENT" % server.upper()
            ).first().value
            max = Cache.query.filter_by(
                key="MC_%s_USERS_MAX" % server.upper()
            ).first().value
            return "%s/%s" % (current, max)
        def pretty_playertime(seconds):
            hours = seconds / 3600.0
            h = seconds / 3600
            m = int((hours - h) * 60)
            return '%sh %sm' % (str(h), str(m))
        return dict(
            get_players=get_players,
            get_status=get_status,
            pretty_playertime=pretty_playertime)

    @application.errorhandler(404)
    @application.errorhandler(500)
    def error(error):
        options = {
            'title': 'Oh no! %s' % error.message,
            'error': error,
        }
        return render_template('error.html', **options), error.code
