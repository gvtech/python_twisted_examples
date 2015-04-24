import sys
from Tkinter import *
from math import sqrt

from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from json import loads,dumps
from twisted.python import log
from twisted.internet import tksupport, reactor


class PositionClientProtocol(WebSocketClientProtocol):
    def onOpen(self):
        print("WebSocket connection open.")
        self.uid = None
        self.factory.client=self

    def sendPosition(self,x,y):
        print "sending position %d,%d"%(x,y)
        self.sendMessage(dumps({"uid":self.uid,"x":x,"y":y}))


    def onMessage(self, payload, isBinary):
        print("Text message received:"+payload)
        pos = loads(payload)
        if "setuid" in pos:
            self.uid=pos["setuid"]
            print "uid %d"%self.uid
        elif pos["uid"]!=self.uid:
            self.factory.callback(pos["uid"],pos["x"],pos["y"])

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


class PositionFactory(WebSocketClientFactory):
    protocol = PositionClientProtocol

    def __init__(self,callback):
        self.callback = callback
        return super(PositionFactory,self).__init__("ws://localhost:9000", debug=False)


class Snake(object):
    def __init__(self,canvas,color):
        self.canvas=canvas
        self.color=color
        self.snake=[]

    def draw_oval(self,x,y,color):
        self.canvas.create_oval(x-5,y-5,x+5,y+5, fill = color, outline=color)

    def paint(self, x,y ):
       self.draw_oval(x,y,self.color)
       self.snake.append( (x,y) )
       if len(self.snake)>30:
            x, y =self.snake.pop(0)
            self.draw_oval( x, y,"#ffffff")

class World(object):
    def __init__(self,master):
        self.master=master
        self.factory=None
        self.canvas = Canvas(master,width=500,height=500)
        self.canvas.pack(expand = YES, fill = BOTH)
        self.canvas.bind( "<Motion>", self.move )
        self.localsnake=Snake(self.canvas,"#028002")
        self.remotesnakes={}

    def move(self, event ):
        if len(self.localsnake.snake)==0:
            self.localsnake.paint(event.x,event.y)
        else:
           px,py=self.localsnake.snake[-1]
           if sqrt((event.x-px)**2+(event.y-py)**2)>= 6 and self.factory is not None and self.factory.client is not None:
                self.factory.client.sendPosition(event.x,event.y)
           while sqrt((event.x-px)**2+(event.y-py)**2)>= 6:
                r=6/sqrt((event.x-px)**2+(event.y-py)**2)
                px=px+(event.x-px)*r
                py=py+(event.x-py)*r
                self.localsnake.paint(px,py)

    def setposition(self,uid,x,y):
        if uid not in self.remotesnakes:
            self.remotesnakes[uid]=Snake(self.canvas,"#800202")
        self.remotesnakes[uid].paint(x,y)

log.startLogging(sys.stdout)
master = Tk()
tksupport.install(master)
master.title( "Multiuser snake" )
world=World(master)
world.factory=PositionFactory(world.setposition)
reactor.connectTCP("localhost",9000,world.factory)


print "running reactor"
reactor.run()
