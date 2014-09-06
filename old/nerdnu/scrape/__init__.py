from nerdnu import app
import json
import nerdnu
import os
import re
import reddit

data_dir = re.sub('/([^/]+)$', '/data', os.path.dirname(__file__))

def write_json(filename, data):
    write_raw(filename, json.dumps(data, indent=4))

def write_raw(filename, data):
    with open(os.path.join(data_dir, filename), 'w') as handle:
        handle.write(data)

#db = sqlite3.connect(app.config['DATABASE'])

import subreddit, wiki, github, query, logs
