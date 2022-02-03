#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Additional modifications by https://github.com/jjpatric
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse

USER_AGENT = "curl/7.68.0"

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = socket.gethostbyname(host)
        self.socket.connect((remote_ip, port))
        return None

    def get_code(self, data):
        ss = data.split()
        if len(ss) > 3:
            return ss[1]
        return 501

    def get_headers(self,data):
        return ""

    def get_body(self, data):
        ss = data.split('\r\n\r\n')
        if len(ss) < 2:
            return ""
        else:
            return ss[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        for _ in range(1):
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # Send get request to server
        parsed_url = urlparse(url)
        # print("URL PARSED: ", parsed_url)
        # print("PORT: ", parsed_url.port)
        http_get = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nAccept: */*\r\n\r\n".format(parsed_url.path, parsed_url.hostname, USER_AGENT)
        print(http_get)

        if not parsed_url.port:
            self.connect(parsed_url.hostname, 80)
        else:
            self.connect(parsed_url.hostname, parsed_url.port)
        self.sendall(http_get)

        # handle reply
        recieved_data = self.recvall(self.socket)
        # print("RECIEVED: \n", recieved)
        code = self.get_code(recieved_data)
        print("GOT CODE: ", code)
        headers = self.get_headers(recieved_data)
        body = self.get_body(recieved_data)
        print("GOT BODY: ", body)
        self.socket.shutdown(socket.SHUT_WR)
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 404
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
