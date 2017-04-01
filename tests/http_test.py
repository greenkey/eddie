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


def send_to_http_bot(bot, in_message):
    conn = HTTPConnection("127.0.0.1:8000")
    conn.request("GET", "/process?" + urlencode({"in_message": in_message}))
    response = conn.getresponse()
    conn.close()
    return response


def test_http_interface(create_bot):
    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message[::-1]

    bot = create_bot(MyBot, HttpEndpoint)

    test_messages = ["hello", "another message"]
    for tm in test_messages:
        r = send_to_http_bot(bot, tm)

        assert r.status == 200
        ret = json.loads(r.read().decode())
        assert ret["out_message"] == tm[::-1]


def test_http_command(create_bot):
    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message[::-1]

        @command
        def start(self):
            return "Welcome!"

    bot = create_bot(MyBot, HttpEndpoint)

    resp = send_to_http_bot(bot, "/start")

    assert resp.status == 200
    ret = json.loads(resp.read().decode())
    assert ret["out_message"] == "Welcome!"


def test_second_session_uses_random_port():
    bot1 = Bot()
    ep = HttpEndpoint()
    bot1.add_endpoint(ep)
    bot1.run()

    bot2 = Bot()
    ep = HttpEndpoint()
    bot2.add_endpoint(ep)
    bot2.run()

    assert bot1.endpoints[0]._PORT != bot2.endpoints[0]._PORT

    resp = send_to_http_bot(bot1, "/start")
    assert resp.status == 200

    resp = send_to_http_bot(bot2, "/start")
    assert resp.status == 200

    bot1.stop()
    bot2.stop()
