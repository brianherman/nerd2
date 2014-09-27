import requests


class Source(object):
    config = object
    def __init__(self, config):
        self.config = config

    def api_call(self, method, **kwargs):
        if method == "update_cache":
            payload = {'key': kwargs['key'], 'value': kwargs['value']}
            requests.post(self.config.API_URL+'update_cache', data=payload)
        if method == "update_creations":
            payload = {'json': kwargs['json']}
            requests.post(self.config.API_URL+'update_creations', data=payload)
        if method == "update_modreqs":
            payload = {'json': kwargs['json']}
            r = requests.post(self.config.API_URL+'update_modreqs', data=payload)
        if method == "update_player_times":
            payload = {'json': kwargs['json']}
            requests.post(self.config.API_URL+'update_player_times', data=payload)


import wiki, mumble, irc, mc_ping, top_players, reddit, forums, staff, modreq

source_packages = [
    wiki,
    mumble,
    irc,
    mc_ping,
    top_players,
    reddit,
    forums,
    staff,
    modreq
]

sources = [p.source for p in source_packages]
