## python_twisted_examples
Some exemple of code using python twisted
This examples was the support of a meetup presentation:
http://www.meetup.com/Groupe-dutilisateurs-Python-Grenoble/events/220731341/

## Defered
- testdefer.py basic example of defer and usage in the inlineCallback

## HTTP:
- httpclient.py exemple
- locator.py IP locator exemple using defer
- locator_inline.py IP locator exemple using inlineCallback
- basic_http_server.py a simple http server equivaltent to SimpleHTTPServer but more robust

## Simple position sharing:
- positionserver.py position sharing server using LineReceiver prototcol
- snake.py simple game using positionserver to share snake position
- wsserver.py position sharing server using Websocket (need Autobahn package) coupled with a classical http server
- wsclient.py position sharing game using web socket
- snake.html browser version of the game

## Proxy Server:
- simpleproxy.py Basic Proxy servereasy to extend to serve your needs



