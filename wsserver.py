
import sys
import json
from twisted.web import static, server
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol,WebSocketServerFactory

class PositionServerProtocol(WebSocketServerProtocol):
    def onOpen(self):

        log.info("WebSocket connection open.")
        self.users = self.factory.users
        self.factory.maxuid+=1
        self.uid = self.factory.maxuid
        self.users[self.uid]=self
        self.sendMessage(json.dumps({"setuid":self.uid}))

    def onClose(self, wasClean, code, reason):
        try:
            if self.uid in self.users:
                del self.users[self.uid]
        except:
            pass

    def onMessage(self, payload, isBinary):
        obj=json.loads(payload)
        if "uid" in obj and obj["uid"] not in self.users:
            self.uid=obj["uid"]
            self.users[self.uid]=self

        for name, protocol in self.users.iteritems():
            if protocol != self:
                print "sending to: %d"%name
                protocol.sendMessage(payload)

class WebSocketPositionFactory(WebSocketServerFactory):
    protocol = PositionServerProtocol

    def __init__(self,url):
        self.users = {} # maps user names to Chat instances
        self.maxuid=0
        return super(WebSocketPositionFactory,self).__init__(url)



if __name__ == '__main__':


    log.startLogging(sys.stdout)

    reactor.listenTCP(8080, server.Site(static.File("./htdocs")))
    reactor.listenTCP(9000, WebSocketPositionFactory("ws://localhost:9000"))
    reactor.run()
