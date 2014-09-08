
import json

from twisted.internet import reactor, task
from twisted.internet.protocol import ClientFactory, Protocol

from scrape.sources import Source

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


class MinecraftPingSource(Source):
    def start(self):
        task.LoopingCall(self.update).start(15)

    def update(self):
        servers = ["c.nerd.nu", "s.nerd.nu", "p.nerd.nu"]
        for server in servers:
            factory = MinecraftPingFactory()
            factory.got_data = self.got_data
            reactor.connectTCP(server, 25565, factory)

    def got_data(self, data):
        if "Creative" in data['description']:
            server="CREATIVE"
        elif "Survival" in data['description']:
            server="SURVIVAL"
        elif "PvE" in data['description']:
            server="PVE"
        else:
            return
        self.api_call("update_cache",
            key="MC_"+server+"_USERS_CURRENT",
            value=data['players']['online'])
        self.api_call("update_cache",
            key="MC_"+server+"_USERS_MAX",
            value=data['players']['max'])

source = MinecraftPingSource
