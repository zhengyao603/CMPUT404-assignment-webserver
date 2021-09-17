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
        # recieve data from client
        self.data = self.request.recv(1024).strip()

        print("Got a request of: %s\n" % self.data.decode())

        # check if the request is GET method
        if self.data.decode().split(' ')[0] != 'GET':
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))
            return

        # security check
        local_url = self.data.decode().split(' ')[1]
        if len((local_url.split('/'))) > 3:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))

        # if it is a path
        if local_url[-1] == '/':
            # check if the path is valid
            if os.path.isdir('./www' + local_url) == False:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))
            else:
                # send back the html file to client
                fd = os.open('./www' + local_url + 'index.html', os.O_RDONLY)
                content = os.read(fd, 1024).decode()
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/html" + "\n\n" + content, "utf-8"))

        # if it is a file
        else:
            # check if the file exist
            if os.path.isfile('./www' + local_url) == False:
                # if the file does not exist, check if it is meant to be a directory
                if os.path.isdir('./www' + local_url + '/') == True:
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nContent-Type:text/css" + "\n\n" + "", "utf-8"))
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type:text/css" + "\n\n" + "", "utf-8"))
            else:
                # send back the reuired html/css file
                fd = os.open('./www' + local_url, os.O_RDONLY)
                content = os.read(fd, 1024).decode()
                if local_url.split('/')[-1] == 'index.html':
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/html" + "\n\n" + content, "utf-8"))
                else:
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/css" + "\n\n" + content, "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
