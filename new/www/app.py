from flask import Flask, render_template

app = Flask(__name__)

from www import blueprints, util, models #config, blueprints, util

for blueprint in blueprints.blueprints:
    app.register_blueprint(blueprint)

@app.errorhandler(404)
@app.errorhandler(500)
def error(error):
    options = {
        'title': 'Oh no! %s' % error.message,
        'error': error,
    }
    return render_template('error.html', **options), error.code
