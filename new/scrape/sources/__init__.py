import requests

class Source(object):
    config = None
    def __init__(self, config):
        self.config = config

    def api_call(self, method, **kwargs):
        if method == "update_cache":
            payload = {'key': kwargs['key'], 'value': kwargs['value']}
            requests.post('http://107.161.23.181:5000/api/update_cache', data=payload)
        if method == "update_creation":
            payload = {'name': kwargs['name'], 'server': kwargs['server'],
                'revision': kwargs['revision'], 'x': kwargs['x'], 'z': kwargs['z']}
            requests.post('http://107.161.23.181:5000/api/update_creation', data=payload)

from scrape.sources import wiki, mumble, irc, mc_ping, top_players, reddit, forums

source_packages = [
    wiki,
    mumble,
    irc,
    mc_ping,
    top_players,
    reddit,
    forums
]

sources = [p.source for p in source_packages]
