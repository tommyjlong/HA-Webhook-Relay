#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler,HTTPServer
import requests
import logging
import logging.handlers #Needed for Syslog
import sys

#Change the following to fit your needs:
HA_URL1 = "https://<IPADDRESS_OR_DNS_OF_HA>:<HA_PORT>"
PORT_NUMBER = <PORT_TO_LISTEN_ON_FROM_CAMERA>

# Setup Logger for this server.
#   If you want to see output to the Console, set CONSOLE = 1
#     Otherwise logs go to local syslog server.
#   If you want debug level output, then change the last
#      _LOGGER.setLevel from NOTSET to DEBUG (i.e. uncomment one, comment the other).
CONSOLE = 0
_LOGGER = logging.getLogger(__name__)
if CONSOLE:
    formatter = \
        logging.Formatter('%(message)s')
    handler1 = logging.StreamHandler(sys.stdout)
    handler1.setFormatter(formatter)
    handler1.setLevel(logging.NOTSET)
    _LOGGER.addHandler(handler1)
else:
    formatter2 = \
        logging.Formatter('%(levelname)s %(asctime)s %(filename)s - %(message)s')
    handler2 = logging.handlers.SysLogHandler(address = '/dev/log')
    handler2.setFormatter(formatter2)
    handler2.setLevel(logging.NOTSET)
    _LOGGER.addHandler(handler2)

#_LOGGER.setLevel(logging.DEBUG)
_LOGGER.setLevel(logging.NOTSET)

def HAPost(url, path):
    """Send http/https POST to home assistant with api """
    url = url + path
    try:
        response = requests.post(url)
       #print(url, response)
        _LOGGER.debug("Sending URL: %s", url)
        _LOGGER.debug("Response: %s", response)
        if str(response) == '<Response [201]>':
            return 1
    except(requests.exceptions.Timeout):
        #HA is slow, just keep retrying
       #print('requests.exceptions.Timeout')
        _LOGGER.error("REQUESTS.TIMEOUT")
        pass #do nothing
    except(requests.exceptions.ConnectionError):
       #print('REQUESTS.CONNECTION_ERROR to ',url)
        _LOGGER.error("REQUESTS.CONNECTION_ERROR to %s",url)
        return 1


#Handle an incoming request
class myHandler(BaseHTTPRequestHandler):
    """Handle the incoming HTTP GET or POST Request."""

    def process_incoming(self):
        """Process the incoming request."""
       #print("Path ", self.path)
       #print("Headers: ", self.headers)
        _LOGGER.debug("Received Path: %s", self.path)
        _LOGGER.debug("Received Headers: %s", self.headers)
        sendReply = False
        position = self.path.find("/api/webhook/")
        if position == -1:
           #print("api/webhook/ portion of URL Not Found")
            _LOGGER.warning("/api/webhook/ portion of URL Not Found")
        else:
            sendReply = True
            url = HA_URL1
            HAPost(url, self.path)

        if sendReply == True:
           #self.send_response(204) #Vivent doesn't like
            self.send_response(200)
            #Must return something to vivint even if null.
            mimetype='text/html'
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write(str.encode('')) #encode string to bytes

        else:
            self.send_error(404,'The requested URL was not found: %s' % self.path)
        return

    def do_GET(self):
        """Process incoming GET requests."""
        return self.process_incoming()

    def do_POST(self):
        """Process incoming POST requests."""
        return self.process_incoming()
    def log_message(self, format, *args):
        """
        Remove this method if you want to see
        normal http.server output, otherwise
        override the http.server output with
        your own logger.
        """
        _LOGGER.debug("%s - - [%s] %s\n" %
                       (self.client_address[0],
                        self.log_date_time_string(),
                        format%args))
        return

try:
    #Create and startup the server and define the handler to manage
    #  the incoming http requests.
    server = HTTPServer(('', PORT_NUMBER), myHandler)
   #print('Started httpserver on port ',  PORT_NUMBER)
    _LOGGER.info("Started http server on port: %s", PORT_NUMBER)

    #Run forever
    server.serve_forever()

except KeyboardInterrupt:
   #print(' received, shutting down the server')
    _LOGGER.info(' received, shutting down the server')
   #print( '^C received, shutting down the server')
finally:
   #print("Closing the socket.  We're Done!")
    _LOGGER.info("Closing the socket.  We're Done!")
    server.socket.close()



