from flask import Blueprint

from www.util import render_with_header

blueprint = Blueprint('wiki', __name__, template_folder='templates')

@blueprint.route('/rules')
def rules():
    return render_with_header("wiki.html")