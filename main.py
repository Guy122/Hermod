from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import cgi
import os
from message import Message
import mysql.connector
from ldap3 import Server, Connection, ALL, SIMPLE, MODIFY_REPLACE

# curl -d '''{"mdn":"+9728878017","networkName":"DD8889","accountId":"HFC_LAB","subscriptionType":"2","payType":"0","corporateName":"HFC_LAB","subsClientType":"1","pairingInd":"1","addPackageInfo":"'{"tierPkgId":"TIER2"}'"}''' -H "Content-Type: application/json" -X POST localhost:8004

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        m = self.rfile.read(length).decode("utf-8")

        m1 = Message(m)
        m1.GetUsers()
        self.wfile.write(m1.JSONResponse["message"].encode())
        # print(m1.JSONResponse["message"])

        return

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        m = self.rfile.read(length).decode("utf-8")

        # if self.path == '/provision/subs':
        m1 = Message(m)
        CheckSyntext = m1.CheckSyntext()
        if CheckSyntext == 0:
            print(m1.Response)
            self.wfile.write(m1.Response.encode())
        else:
            m1.Create()
            self.wfile.write(m1.Response.encode())
            print(m1.Response)

    def do_PUT(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        length = int(self.headers.get('content-length'))
        m = self.rfile.read(length).decode("utf-8")
        m1 = Message(m)
        CheckSyntext = m1.CheckSyntext()
        if CheckSyntext == 0:
            print(m1.Response)
            self.wfile.write(m1.Response.encode())
        else:
            m1.Update()
            self.wfile.write(m1.Response.encode())
            print(m1.Response)

    def do_DELETE(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        length = int(self.headers.get('content-length'))
        m = self.rfile.read(length).decode("utf-8")
        m1 = Message(m)
        CheckSyntext = m1.CheckSyntext()
        if CheckSyntext == 0:
            print(m1.Response)
            self.wfile.write(m1.Response.encode())
        else:
            m1.Delete()
            self.wfile.write(m1.Response.encode())
            print(m1.Response)


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8004), RequestHandler)
    print('Starting server at http://localhost:8004')
    server.serve_forever()
