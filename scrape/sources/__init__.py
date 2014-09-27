import requests


class Source(object):
    config = object
    def __init__(self, config):
        self.config = config

    def api_call(self, method, **kwargs):
        if method == "update_cache":
            payload = {'key': kwargs['key'], 'value': kwargs['value']}
            requests.post(self.config.API_URL+'update_cache', data=payload)
        if method == "update_creation":
            payload = {'name': kwargs['name'], 'server': kwargs['server'],
                'revision': kwargs['revision'], 'x': kwargs['x'], 'z': kwargs['z']}
            requests.post(self.config.API_URL+'update_creation', data=payload)
        if method == "update_modreq":
            r = requests.post(self.config.API_URL+'update_modreq', data=kwargs)
        if method == "update_playertime":
            payload = {'playername': kwargs['playername'], 'server': kwargs['server'], 'seconds': kwargs['seconds']}
            requests.post(self.config.API_URL+'update_playertime', data=payload)


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
