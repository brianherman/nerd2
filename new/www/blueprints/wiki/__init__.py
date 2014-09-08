from flask import Blueprint, render_template
from www.models.cache import Cache

blueprint = Blueprint('wiki', __name__, template_folder='templates')

@blueprint.route('/rules')
def rules():
    body = Cache.query.filter_by(key='HTML_RULES').first()
    return render_template("wiki.html", body=body.value)
