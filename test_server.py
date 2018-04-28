import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

home_path = "test_pages" + os.sep


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        rpage = self.path.strip("/")
        if rpage in os.listdir(home_path):
            index = open(home_path + rpage, "r").read()

            self.send_response(200)

            # Then send headers.
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # Then encode and send the form.
            self.wfile.write(index.encode())


server_address = ('', 3117)
httpd = HTTPServer(server_address, HttpHandler)
httpd.serve_forever()
