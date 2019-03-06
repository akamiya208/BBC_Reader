# -*- coding: utf-8 -*-

import http.server

def run(server_class, handler_class):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

PORT = 8000
server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
run(server,handler)