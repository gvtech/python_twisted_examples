import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.web import proxy, http

class LoggingProxyRequest(proxy.ProxyRequest):
    def process(self):
        log.msg(self.method+" "+self.uri)
        for header,value in self.getAllHeaders().iteritems():
            log.msg("%s:%s"%(header,value))
        try:
            proxy.ProxyRequest.process(self)
        except KeyError:
            print "HTTPS is not supported at the moment!"

class LoggingProxy(proxy.Proxy):
    requestFactory = LoggingProxyRequest

class LoggingProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return LoggingProxy()


log.startLogging(sys.stdout)
reactor.listenTCP(3128, LoggingProxyFactory())
reactor.run()
