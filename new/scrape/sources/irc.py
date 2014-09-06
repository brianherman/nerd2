import re

from twisted.internet import reactor, task
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

from scrape.sources import Source

class IRCProtocol(LineReceiver):
    def connectionMade(self):
        self.sendLine("NICK FooBot")
        self.sendLine("USER bot bot bot :bot")

    def connectionLost(self, reason=None):
        self.factory.stopFactory()

    def lineReceived(self, line):
        ping = re.match(r'^PING :(.*)', line)
        if ping:
            self.sendLine("PONG :%s" % ping.group(1))
            return

        welcome = re.match(r'^:\S+ 002', line)
        if welcome:
            self.sendLine("LIST #RedditMC")
            return

        list_ = re.match(r'^:\S+ 322 (\S+) (\S+) (\d+)', line)
        if list_:
            self.factory.got_users(int(list_.group(3)))
            self.sendLine("QUIT :quit")
            self.transport.loseConnection()



class IRCFactory(ClientFactory):
    protocol = IRCProtocol


class IRCSource(Source):
    def start(self):
        task.LoopingCall(self.update).start(10*60)
    def update(self):
        factory = IRCFactory()
        factory.got_users = self.got_users
        reactor.connectTCP("irc.gamesurge.net", 6667, factory)

    def got_users(self, count):
        self.api_call("update_cache",
            key="IRC_USERS_CURRENT",
            value=count)

source = IRCSource