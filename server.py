#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        conn = self.request
        data = conn.recv(1024).decode('utf-8')

        string_list = data.split(' ')     
        method = string_list[0]
        filepath = string_list[1].split('?')[0] 
        filepath.strip('/')  
        filepath = os.path.join("./www/", filepath.lstrip('/'))
        redirected = False  
        if os.path.exists(filepath.strip('/')+'/index.html'):
            if not filepath.endswith('/'):
                redirected = True
            filepath += '/index.html'

        if method == "GET":
            try:
                file = open(filepath,'rb') 
                payload = file.read()
                header = 'HTTP/1.1 200 OK\n'
        
                if(filepath.endswith(".css")):
                    ftype = 'text/css'
                else:
                    ftype = 'text/html'

                if redirected:
                    header = 'HTTP/1.1 301 Moved Permanently\nContent-Type: %s\n\n' % (ftype, )
                else:
                    header = 'HTTP/1.1 200 OK\nContent-Type: %s\n\n'% (ftype, )
                file.close()
            
            except Exception as e:
                header = 'HTTP/1.1 404 Not Found\n\n'
                payload = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
        else:
            header = 'HTTP/1.1 405 Method Not Allowed\n\n'
            payload = '<html><body><center><h3>Error 405 Method Not Allowed</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
        
        message = header.encode('utf-8') + payload
        print(message.decode())
        conn.sendall(message)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
