from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.playertime import PlayerTime
from models.cache import Cache

blueprint = Blueprint('usage', __name__, template_folder='templates')

@blueprint.route('/<server>/usage')
def usage(server):
    if server.lower() not in ('creative', 'pve'):
        flash('invalid server')
        return redirect(url_for('server.%s_index' % server.lower()))

    stats = PlayerTime.query.filter_by(server=server).order_by(PlayerTime.seconds.desc()).all()
    online = Cache.query.filter_by(key='MC_%s_ONLINE' % server.upper()).first().value

    return render_template('usage.html',
                           title='usage :: %s' % server,
                           server=server,
                           stats=stats,
                           online=online)
