from __future__ import absolute_import
from http.client import HTTPConnection
import json
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from pychatbot.bot import Bot, command
from pychatbot.endpoints import HttpEndpoint


def test_http_interface():
    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message[::-1]

    bot = MyBot()
    ep = HttpEndpoint()
    bot.add_endpoint(ep)
    bot.run()

    test_messages = ["hello", "another message"]
    for tm in test_messages:
        conn = HTTPConnection("127.0.0.1:8000")
        conn.request("GET", "/process?" + urlencode({"in_message": tm}))
        r = conn.getresponse()
        assert r.status == 200
        ret = json.loads(r.read().decode())
        assert ret["out_message"] == tm[::-1]
        conn.close()

    bot.stop()


def test_http_command():
    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message[::-1]

        @command
        def start(self):
            return "Welcome!"

    bot = MyBot()
    ep = HttpEndpoint()
    bot.add_endpoint(ep)
    bot.run()

    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?in_message=/start")
    resp = conn.getresponse()
    assert resp.status == 200
    ret = json.loads(resp.read().decode())
    assert ret["out_message"] == "Welcome!"
    conn.close()

    bot.stop()


def test_bot_dont_logs_by_default(mocker):
    log_message_m = mocker.patch(
        'pychatbot.endpoints.http.BaseHTTPRequestHandler.log_message')
    bot = Bot()
    ep = HttpEndpoint()
    bot.add_endpoint(ep)
    bot.run()
    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?in_message=/start")
    conn.close()
    bot.stop()

    assert not log_message_m.called


def test_bot_logs_if_set(mocker):
    log_message_m = mocker.patch(
        'pychatbot.endpoints.http.BaseHTTPRequestHandler.log_message')
    bot = Bot()
    ep = HttpEndpoint()
    bot.add_endpoint(ep)
    bot.run()
    bot.logging = True
    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?in_message=/start")
    conn.close()
    bot.stop()

    assert log_message_m.called
