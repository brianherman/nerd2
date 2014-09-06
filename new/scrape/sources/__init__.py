class Source(object):
    config = None
    def __init__(self, config):
        self.config = config

    def api_call(self, method, **kwargs):
        if method == "update_cache":
            print "API: %s %s = %s" % (method, kwargs['key'], kwargs['value'])

from scrape.sources import wiki, mumble, irc

source_packages = [
    wiki,
    mumble,
    irc
]

sources = [p.source for p in source_packages]