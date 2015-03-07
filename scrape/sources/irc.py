import re

from twisted.internet import reactor, task, ssl
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

from OpenSSL import SSL

from sources import Source


class IRCProtocol(LineReceiver):
    def connectionMade(self):
        self.sendLine("NICK %s" % self.config.IRC_NICK)
        self.sendLine("USER %s 0 * :%s" % (self.config.IRC_USER, self.config.IRC_REALNAME))
        self.sendLine("PASS %s:%s" % (self.config.IRC_USER, self.config.IRC_PASSWORD))

    def connectionLost(self, reason=None):
        self.factory.stopFactory()

    def lineReceived(self, line):
        ping = re.match(r'^PING :(.*)', line)
        if ping:
            self.sendLine("PONG :%s" % ping.group(1))
            return

        welcome = re.match(r'^:\S+ 002', line)
        if welcome:
            self.sendLine("LIST %s" % self.config.IRC_CHANNEL)
            return

        list_ = re.match(r'^:\S+ 322 (\S+) %s (\d+)' % self.config.IRC_CHANNEL, line, re.IGNORECASE)
        if list_:
            self.factory.got_users(int(list_.group(2)))
            self.done = True
            self.sendLine("QUIT :quit")
            self.transport.loseConnection()

        list_end = re.match(r'^:\S+ 323', line)
        if list_end and not self.done:
            print "Couldn't get IRC users. Is the channel private or secret?"
            self.factory.got_users(0)
            self.sendLine("QUIT :quit")
            self.transport.loseConnection()

    def __init__(self):
        self.done = False


class IRCFactory(ClientFactory):
    protocol = IRCProtocol


class CtxFactory(ssl.ClientContextFactory):
    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)

        return ctx


class IRCSource(Source):
    def start(self):
        task.LoopingCall(self.update).start(10*60)

    def update(self):
        factory = IRCFactory()
        factory.got_users = self.got_users
        factory.protocol.config = self.config

        if self.config.IRC_SSL:
            reactor.connectSSL(self.config.IRC_SERVER, self.config.IRC_PORT, factory, CtxFactory())
        else:
            reactor.connectTCP(self.config.IRC_SERVER, self.config.IRC_PORT, factory)

    def got_users(self, count):
        self.api_call("update_cache",
            key="IRC_USERS_CURRENT",
            value=count)


source = IRCSource
