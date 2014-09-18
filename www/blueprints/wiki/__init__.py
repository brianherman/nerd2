from flask import Blueprint, render_template
from models.cache import Cache

blueprint = Blueprint('wiki', __name__, template_folder='templates')

@blueprint.route('/rules')
def rules():
    body = Cache.query.filter_by(key='HTML_RULES').first().value
    return render_template("wiki.html", body=body, title='rules')

@blueprint.route('/irc')
def irc():
    body = Cache.query.filter_by(key='HTML_IRC').first().value
    return render_template("wiki.html", body=body, title='irc')
