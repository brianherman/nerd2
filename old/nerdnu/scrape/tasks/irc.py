
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

botname = "FooBot"

class MyLineReceiver(LineReceiver):
    def __init__(self):
        pass

    def connectionMade(self):
        self.sendLine("NICK %s" % botname)
        self.sendLine("USER %s %s %s :%s" % (botname, botname, botname, botname))
        self.sendLine("LIST #redditmc")

    def lineReceived(self, line):
        print line
        cmd, data = line.split(" ", 1)
        if cmd == "PING":
            self.sendLine("PONG %s" % data)



class MyFactory(ClientFactory):
    protocol = MyLineReceiver



reactor.connectTCP("irc.gamesurge.net", 6667, MyFactory())
reactor.run()