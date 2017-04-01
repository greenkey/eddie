from __future__ import absolute_import
from http.client import HTTPConnection
import json
import pytest
from time import sleep
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from pychatbot.bot import Bot, command
from pychatbot.endpoints import HttpEndpoint


@pytest.fixture
def create_bot(request):

    fixture = dict()

    def create(bot_class, http_class):
        fixture['bot'] = bot_class()
        fixture['ep'] = http_class()
        fixture['bot'].add_endpoint(fixture['ep'])
        fixture['bot'].run()

        return fixture['bot']

    yield create

    fixture['bot'].stop()


def test_http_interface(create_bot):
    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message[::-1]

    create_bot(MyBot, HttpEndpoint)

    test_messages = ["hello", "another message"]
    for tm in test_messages:
        conn = HTTPConnection("127.0.0.1:8000")
        conn.request("GET", "/process?" + urlencode({"in_message": tm}))
        r = conn.getresponse()
        assert r.status == 200
        ret = json.loads(r.read().decode())
        assert ret["out_message"] == tm[::-1]
        conn.close()


def test_http_command(create_bot):
    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message[::-1]

        @command
        def start(self):
            return "Welcome!"

    create_bot(MyBot, HttpEndpoint)

    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?in_message=/start")
    resp = conn.getresponse()
    assert resp.status == 200
    ret = json.loads(resp.read().decode())
    assert ret["out_message"] == "Welcome!"
    conn.close()


def test_bot_dont_logs_by_default(mocker, create_bot):
    log_message_m = mocker.patch(
        'pychatbot.endpoints.http.BaseHTTPRequestHandler.log_message')
    create_bot(Bot, HttpEndpoint)

    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?in_message=/start")
    conn.close()
    sleep(0.5)

    assert not log_message_m.called


def test_bot_logs_if_set(mocker, create_bot):
    log_message_m = mocker.patch(
        'pychatbot.endpoints.http.BaseHTTPRequestHandler.log_message')

    bot = create_bot(Bot, HttpEndpoint)

    bot.logging = True

    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?in_message=/start")
    conn.close()
    sleep(0.5)

    assert log_message_m.called
