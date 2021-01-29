# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler # python3
class HandleRequests(CGIHTTPRequestHandler):


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(b"received get request")
        print(self.path)
    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.wfile.write("received post request:<br>{}".format(post_body))

    def do_PUT(self):
        self.do_POST()

host = ''
port = 8081
HTTPServer((host, port), HandleRequests).serve_forever()
