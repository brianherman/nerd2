import json
import urllib
import math

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class TopPlayersSource(Source):

    def _query(self, server, **request_data):
        d0 = defer.Deferred()

        def _callback(d):
            d0.callback(json.loads(d.decode('utf8')))

        def _errback(e):
            d0.errback(e)

        args = {'data': ''}
        args.update(request_data)
        url = 'http://nerd.nu/usage/'+server+'/index.php?' + urllib.urlencode(args)

        d1 = client.getPage(url)
        d1.addCallbacks(_callback, _errback)

        return d0

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        for server in ("creative", "survival", "pve"):
            d = self._query(server)
            d.addCallback(self._handle_stats, server)

    def _handle_stats(self, response_data, server):
        raw_data = response_data['storage']['usagestats']
        data = json.loads(raw_data)['players']

        for playername,times in data.items():
            seconds = times['min'] / 1000
            self.api_call("update_playertime", playername=playername, server=server, seconds=seconds)


source = TopPlayersSource
