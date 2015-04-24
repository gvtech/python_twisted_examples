from twisted.internet import reactor
from twisted.internet.defer import Deferred,inlineCallbacks

def double(i):
    print "double"
    return i*2

def incr(i):
    print "incr"
    return i+1

def square(i):
    print "square"
    return i*i

def print_result(i):
    print 'Result:'+str(i)

def proc_A(i):
    print "\nproc_A"
    d = Deferred()
    d.addCallback(double)
    d.addCallback(incr)
    d.addCallback(square)
    d.addCallback(print_result)
    return d.callback(i)

@inlineCallbacks
def proc_B(i):
    print "\nproc_B"
    v1 = yield double(i)
    v2 = yield incr(v1)
    v3 = yield square(v2)
    print_result(v3)

reactor.callLater(0,proc_A,10)
reactor.callLater(1,proc_B,10)

reactor.run()

