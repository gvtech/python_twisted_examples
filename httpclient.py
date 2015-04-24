from twisted.internet import reactor,task
from twisted.python import log
from twisted.web.client import Agent
from datetime import datetime
import sys

log.startLogging(sys.stdout)
logger=log.Logger()

def getUrl(url):
    log.msg("\tGET %s"%(url))
    agent = Agent(reactor)
    req = agent.request('GET',url)
    reqtime=datetime.now()
    req.addCallback(gotResponse,url,reqtime)
 #   return req

def gotResponse(response,url,reqtime):
    resptime=datetime.now()-reqtime
    log.msg("\tResponse to %s\t%d\tin: %d"%(url,response.code,resptime.microseconds))


urls=["http://localhost:8080/snake.html",
      "http://localhost:8080/httpclient.py",
      "http://localhost:8080/basic_twisted_http_server.py",
      "http://localhost:8080/missing.html"]

def doSomething():
    if len(urls)>0:
        url=urls.pop(0)
        reactor.callLater(0.01,getUrl,url)

def endsAll(loop):
    log.msg("Stopping")
    loop.stop()
    reactor.stop()


l=task.LoopingCall(doSomething)
l.start(0.1)
reactor.callLater(10,endsAll,l)
reactor.run()

