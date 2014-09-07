from flask import Blueprint, render_template

blueprint = Blueprint('wiki', __name__, template_folder='templates')

@blueprint.route('/rules')
def rules():
    return render_template("wiki.html")
