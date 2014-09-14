import json
import urllib
import feedparser

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class ForumsSource(Source):

    def _query(self, **request_data):
        d0 = defer.Deferred()

        def _callback(d):
            d0.callback(feedparser.parse(d.decode('utf8')))

        def _errback(e):
            d0.errback(e)

        url = 'https://nerd.nu/forums/index.php?/rss/forums/5-all-discussions/'

        d1 = client.getPage(url)
        d1.addCallbacks(_callback, _errback)

        return d0

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        d = self._query()
        d.addCallback(self._handle_posts)

    def _handle_posts(self, response_data):
        posts = []
        post_count = 0
        for post in response_data.entries:
            if post_count == 25:
                break
            posts.append({
                'url': post.link,
                'title': post.title
            })
            post_count += 1
        posts = json.dumps(posts)
        self.api_call("update_cache", key="FORUM_POSTS", value=posts)


source = ForumsSource
