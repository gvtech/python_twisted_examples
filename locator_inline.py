from twisted.internet import reactor
from twisted.python import log
from twisted.web.client import getPage
from twisted.internet.defer import inlineCallbacks,returnValue

import re
import sys
import json

# to test this example get a key from https://db-ip.com/api/
DB_IP_KEY="enter you key here"


log.startLogging(sys.stdout)
logger=log.Logger()

@inlineCallbacks
def getMyIp():
    log.msg("Getting my IP")
    response= yield getPage('http://checkip.dyndns.org')
    log.msg("check IP response:"+response.__repr__())
    ip=re.compile("Current IP Address: ([0-9,\.]+)").search(response).group(1)
    returnValue(ip)

@inlineCallbacks
def locateIp(ip):
    log.msg("locating IP: "+ip)
    locjson= yield getPage("http://api.db-ip.com/addrinfo?addr=%s&api_key=%s"%(ip,DB_IP_KEY))
    log.msg(locjson)
    loc=json.loads(locjson)
    returnValue(loc)

@inlineCallbacks
def whereIsMyIp():
    ip = yield getMyIp()
    loc= yield locateIp(ip)
    print "My IP is in: %s (%s)"%(loc["city"],loc["country"])

reactor.callLater(0,whereIsMyIp)
reactor.run()


