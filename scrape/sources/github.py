import json
import urllib
import math

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class GithubSource(Source):

    def _query(self, **request_data):
        d0 = defer.Deferred()

        def _callback(d):
            d0.callback(json.loads(d.decode('utf8')))

        def _errback(e):
            d0.errback(e)

        headers = {'Accept': 'application/vnd.github.v3+json'}
        args = {'state': 'open'}
        args.update(request_data)
        url = 'https://api.github.com/repos/nerdnu/nerdbugs/issues?' + urllib.urlencode(args)

        d1 = client.getPage(url, headers=headers)
        d1.addCallbacks(_callback, _errback)

        return d0

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        for server in ("creative", "survival", "pve"):
            d = self._query(labels=server)
            d.addCallback(self._handle_issues, server)

    def _handle_issues(self, response_data, server):
        issues = []
        for issue in response_data:
            issues.append({
                'url': issue['url'],
                'title': issue['title'],
                'author': issue['user']['login'],
                'num_comments': issue['comments']
            })
        issues = json.dumps(issues)
        self.api_call("update_cache", key="GITHUB_"+server.upper()+"_ISSUES", value=issues)


source = GithubSource
