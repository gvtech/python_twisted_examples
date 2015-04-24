from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json

class PositionServer(LineReceiver):

    def __init__(self, users,uid):
        self.users = users
        self.uid = uid

    def connectionMade(self):
        print "new connection made %d"%self.uid
        self.users[self.uid]=self
        self.sendLine(json.dumps({"setuid":self.uid}))

    def connectionLost(self, reason):
        if self.uid in self.users:
            del self.users[self.uid]

    def lineReceived(self, line):
        print line
        obj=json.loads(line)
        if "uid" in obj and obj["uid"] not in self.users:
            self.uid=obj["uid"]
            self.users[self.uid]=self

        for name, protocol in self.users.iteritems():
            if protocol != self:
                print "sending to: %d"%name
                protocol.sendLine(line)


class PositionFactory(Factory):
    def __init__(self):
        self.users = {} # maps user names to Chat instances
        self.maxuid=0

    def buildProtocol(self, addr):
        self.maxuid+=1
        return PositionServer(self.users,self.maxuid)

reactor.listenTCP(8123, PositionFactory())
reactor.run()

