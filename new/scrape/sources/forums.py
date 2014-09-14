import json
import urllib
import feedparser

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class ForumsSource(Source):

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        url = 'https://nerd.nu/forums/index.php?/rss/forums/5-all-discussions/'
        d = client.getPage(url)
        d.addCallback(self._handle_posts)

    def _handle_posts(self, response_data):
        response_data = feedparser.parse(response_data.decode('utf8'))

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
