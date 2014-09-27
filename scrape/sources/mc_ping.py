import json

from twisted.internet import reactor, task
from twisted.internet.protocol import ClientFactory, Protocol

from sources import Source


class MinecraftPingProtocol(Protocol):
    buf = ""
    def connectionMade(self):
        self.transport.write("\x06\x00\x05\x00\x00\x00\x01\x01\x00")

    def connectionLost(self, reason=None):
        self.factory.stopFactory()

    def dataReceived(self, data):
        self.buf += data

        b = self.buf

        try:
            _, b = self.unpackVarint(b) # packet length
            _, b = self.unpackVarint(b) # packet id
            l, b = self.unpackVarint(b)
            if l != len(b):
                raise IndexError()

            data = json.loads(b)
            self.factory.got_data(data)
            self.transport.loseConnection()

        except IndexError:
            pass

    def unpackVarint(self, data):
        o = 0
        for i in range(5):
            d = ord(data[i])
            o |= (d & 0x7F) << 7*i
            if not d & 0x80:
                return o, data[i+1:]


class MinecraftPingFactory(ClientFactory):
    protocol = MinecraftPingProtocol

    def __init__(self, source, server_name):
        self.source = source
        self.server_name = server_name
        self.timeout = reactor.callLater(20, self.timed_out)

    def timed_out(self):
        self.source.server_down(self.server_name)

    def got_data(self, data):
        if self.timeout.active():
            self.timeout.cancel()
        if 'players' in data:
            self.source.server_up(self.server_name,
                                  data['players']['online'],
                                  data['players']['max'])
        else:
            self.source.server_down(self.server_name)



class MinecraftPingSource(Source):
    def start(self):
        task.LoopingCall(self.update).start(30)

    def update(self):
        servers = [
            ("creative", "c.nerd.nu"),
            ("survival", "s.nerd.nu"),
            ("pve", "p.nerd.nu")
        ]
        for server_name, server_addr in servers:
            factory = MinecraftPingFactory(self, server_name.upper())
            reactor.connectTCP(server_addr, 25565, factory)

    def server_up(self, server, users_current, users_max):
        self.api_call("update_cache",
            key = "MC_%s_STATUS" % server,
            value="online")
        self.api_call("update_cache",
            key="MC_%s_USERS_CURRENT" % server,
            value=data['players']['online'])
        self.api_call("update_cache",
            key="MC_%s_USERS_MAX" % server,
            value=data['players']['max'])

    def server_down(self, server):
        self.api_call("update_cache",
            key = "MC_%s_STATUS" % server,
            value="offline")

source = MinecraftPingSource
