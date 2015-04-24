from twisted.internet import reactor
from twisted.python import log
from twisted.web.client import getPage
import re
import sys
import json

# to test this example get a key from https://db-ip.com/api/
DB_IP_KEY="enter you key here"

log.startLogging(sys.stdout)
logger=log.Logger()

def getMyIp():
    log.msg("Getting my IP")
    req = getPage('http://checkip.dyndns.org')
    req.addCallback(getMyIpResponse)
    return req


def getMyIpResponse(response):
    log.msg("check IP response:"+response.__repr__())
    ip=re.compile("Current IP Address: ([0-9,\.]+)").search(response).group(1)
    log.msg("ip:"+ip)
    return ip


def locateIp(ip):
    log.msg("locating IP: "+ip)
    req = getPage("http://api.db-ip.com/addrinfo?addr=%s&api_key=%s"%(ip,DB_IP_KEY))
    req.addCallback(printLocation)

def printLocation(locjson):
    log.msg(locjson)
    loc=json.loads(locjson)
    print "My IP is in: %s (%s)"%(loc["city"],loc["country"])


def whereIsMyIp():
    d1=getMyIp()
    d1.addCallback(locateIp)


reactor.callLater(0,whereIsMyIp)
reactor.run()


