from flask import Flask

from www import config, blueprints, util

app = Flask(__name__)

for blueprint in blueprints.blueprints:
    app.register_blueprint(blueprint)

@app.errorhandler(404)
@app.errorhandler(500)
def error(error):
    options = {
        'title': 'Oh no! %s' % error.message,
        'error': error,
    }
    return util.render_with_header('error.html', **options), error.code
