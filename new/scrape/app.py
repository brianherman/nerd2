from twisted.internet import reactor

import sources

class ScrapeApp(object):
    config = None

    def run(self):
        for source in sources.sources:
            s = source(self.config)
            s.start()
        reactor.run()

app = ScrapeApp()