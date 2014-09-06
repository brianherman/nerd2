from flask import Flask, g
import nerdnu.config
import sqlite3
app = Flask(__name__)
app.config.from_object(nerdnu.config)

# @app.before_request
# def before_request():
    # pass

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


import nerdnu.views
