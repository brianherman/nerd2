import urllib
import requests

from twisted.internet import reactor, task

from twisted.web import client
client.HTTPClientFactory.noisy = False

import sources

class ScrapeApp(object):
    config = None

    def __init__(self):
        self.api_calls = []
        task.LoopingCall(self.tick).start(0.1)

    def run(self):
        for source in sources.sources:
            s = source()
            s.config = self.config
            s.api_call = self.api_call
            s.start()
        reactor.run()

    def tick(self):
        if len(self.api_calls) > 0:
            method, payload = self.api_calls.pop(0)
            #print "sending", method
            #client.getPage(self.config.API_URL+method,
            #               method='post',
            #               postdata=urllib.urlencode(payload),
            #               headers={'Content-Type':'application/x-www-form-urlencoded'})
            requests.post(self.config.API_URL+method, data=payload)

    def api_call(self, method, **kwargs):
        payload = None
        if method == "update_cache":
            #print method, kwargs['key']
            payload = {'key': kwargs['key'], 'value': kwargs['value']}
        elif method == "update_creations":
            payload = kwargs
            #print method, kwargs['name']
        elif method == "update_modreqs":
            payload = kwargs
        elif method == "update_player_times":
            payload = kwargs

        if payload:
            self.api_calls.append((method, payload))
app = ScrapeApp()
