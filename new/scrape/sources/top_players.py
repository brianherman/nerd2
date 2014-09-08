import re
import json
import urllib
import math

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from scrape.sources import Source

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
        ### Creative Stats
        d = self._query('creative')
        d.addCallback(self._handle_creative_stats)

        ### Survival Stats
        d = self._query('survival')
        d.addCallback(self._handle_survival_stats)

        ### PvE Stats
        d = self._query('pve')
        d.addCallback(self._handle_pve_stats)

    def _handle_data(self, data):
        r = data['storage']['usagestats']

        sp = json.loads(r)['players']
        sl = {}
        for k,v in sp.items():
            sl[k] = v['min']
        su = sorted(sl.items(), key=lambda x:x[1], reverse=True)

        stats = []
        count = 0
        for stat in su:
            if count == 10:
                break
            def pretty_time(time):
                hours = time / 3600000.0
                h = time / 3600000
                m =  int((hours - h) * 60)
                return str(h)+'h '+str(m)+'m'
            time = pretty_time(stat[1])
            stats.append({'username': stat[0], 'time': time})
            count = count+1

        return json.dumps(stats)

    def _handle_creative_stats(self, response_data):
        stats = self._handle_data(response_data)
        self.api_call("update_cache", key="MC_CREATIVE_TOP_PLAYERS", value=stats)

    def _handle_survival_stats(self, response_data):
        stats = self._handle_data(response_data)
        self.api_call("update_cache", key="MC_SURVIVAL_TOP_PLAYERS", value=stats)

    def _handle_pve_stats(self, response_data):
        stats = self._handle_data(response_data)
        self.api_call("update_cache", key="MC_PVE_TOP_PLAYERS", value=stats)


source = TopPlayersSource
