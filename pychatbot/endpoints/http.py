from __future__ import absolute_import
from threading import Thread
from time import sleep
from socket import error as socket_error
from http.client import HTTPConnection
import sys


try:
    from urllib.parse import parse_qs
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from urlparse import parse_qs
    import SimpleHTTPServer
    from SocketServer import TCPServer as HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler
    HTTPServer.allow_reuse_address = True
import json
from socket import error as socket_error


class HttpEndpoint(object):
    _PORT = 8000
    _ADDRESS = "localhost"

    def __init__(self):
        class Handler(BaseHTTPRequestHandler, object):
            def do_GET(handler):
                function, params = handler.path.split("?")
                function, params = function[1:], parse_qs(params)
                handler.send_response(200)
                handler.end_headers()
                output = {
                    "out_message": self._bot.process(
                        "".join(params["in_message"])
                    )
                }
                handler.wfile.write(json.dumps(output).encode("UTF-8"))

            def log_message(handler, format_, *args):
                if self._bot.logging:
                    if sys.version_info[:2] > (2, 6):
                        super(Handler, handler).log_message(format_, *args)
                    else:
                        Handler.log_message(handler, format_, *args)

        port_found = False
        while not port_found:
            try:
                self._httpd = HTTPServer((self._ADDRESS, self._PORT), Handler)
                self._http_on = False
                port_found = True
            except OSError:
                self._PORT += 1
            except socket_error:
                self._PORT += 1

    def set_bot(self, bot):
        self._bot = bot

    def serve_loop(self):
        try:
            while self._http_on:
                self._httpd.handle_request()
        except socket_error:
            pass

    def run(self):
        self._http_on = True
        self._http_thread = Thread(target=self.serve_loop)
        self._http_thread.start()

        while not self._http_thread.is_alive():
            sleep(0.5)

    def stop(self):
        self._http_on = False

        conn = HTTPConnection(
            self._ADDRESS + ":" + str(self._PORT)
        )
        conn.request("GET", "/shutdown")
        conn.close()
        while self._http_thread.is_alive():
            sleep(0.5)
            self._httpd.server_close()
            self._httpd.socket.close()
