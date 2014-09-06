import struct

from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol

from scrape.sources import Source

class MumbleProtocol(DatagramProtocol):
    buff = ""

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def ping(self):
        self.transport.write('\x00'*12, addr=(self.host, self.port))

    def datagramReceived(self, data, (host, port)):
        self.buff += data

        if len(self.buff) < 24:
            return

        if not self.buff.startswith('\x00\x01\x02\x03' + '\x00' * 8):
            print "the mumble server gave us crazy data!"

            self.buff = ""
            return

        d = dict(zip(
            ('users_current', 'users_max'),
            struct.unpack('>II', self.buff[12:20])))

        self.buff = self.buff[24:]

        self.got_users(d)


class MumbleSource(Source):
    def start(self):
        p = MumbleProtocol('mumble.nerd.nu', 6162)
        p.got_users = self.got_users
        reactor.listenUDP(0, p)

        task.LoopingCall(p.ping).start(60)

    def got_users(self, d):
        self.api_call('update_cache',
            key="MUMBLE_USERS_CURRENT",
            value=d['users_current'])
        self.api_call('update_cache',
            key="MUMBLE_USERS_MAX",
            value=d['users_max'])

source = MumbleSource