import json
import urllib

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class RedditSource(Source):

    def _query(self, **request_data):
        d0 = defer.Deferred()

        def _callback(d):
            d0.callback(json.loads(d.decode('utf8')))

        def _errback(e):
            d0.errback(e)

        headers = {'User-Agent': 'nerd2 website bot by /u/williammck and /u/barneygale'}
        args = {'sort': 'new', 'restrict_sr': 'on'}
        args.update(request_data)
        url = 'https://www.reddit.com/r/mcpublic/search.json?' + urllib.urlencode(args)

        d1 = client.getPage(url, headers=headers)
        d1.addCallbacks(_callback, _errback)

        return d0

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        d = self._query()
        d.addCallback(self._handle_posts)

    def _handle_posts(self, response_data):
        posts = []
        for post in response_data['data']['children']:
            data = post['data']
            posts.append({
                'url': data['url'],
                'title': data['title'],
                'author': data['author'],
                'num_comments': data['num_comments'],
                'permalink': 'http://www.reddit.com'+data['permalink'],
                'flair': data['link_flair_text']
            })
        posts = json.dumps(posts)
        self.api_call("update_cache", key="REDDIT_POSTS", value=posts)


source = RedditSource
