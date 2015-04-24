
import sys
from twisted.web import static, server
from twisted.python import log
from twisted.internet import reactor

log.startLogging(sys.stdout)

reactor.listenTCP(8080, server.Site(static.File(".")))
reactor.run()
