""" Not-so-unit tests for pychatbot.endpoints.HttpEndpoint
"""

from __future__ import absolute_import
import json
import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from pychatbot.bot import Bot, command
from pychatbot.endpoints import HttpEndpoint


def send_to_http_bot(bot, in_message):
    """ Helper function: send a message to the bot using http
    """

    for endpoint in bot.endpoints:
        address = "http://%s:%d/process?%s" % (
            endpoint.host,
            endpoint.port,
            urlencode({"in_message": in_message})
        )

        return requests.get(address)


def test_http_interface(create_bot):
    """ Test that the http interface uses the bot with the given bot class
    """

    class MyBot(Bot):
        "Reverse bot"

        def default_response(self, in_message):
            return in_message[::-1]

    bot = create_bot(MyBot, HttpEndpoint)

    test_messages = ["hello", "another message"]
    for message in test_messages:
        resp = send_to_http_bot(bot, message)

        assert resp.status_code == 200
        ret = json.loads(resp.text)
        assert ret["out_message"] == message[::-1]


def test_http_command(create_bot):
    """ Test that the http interface correctly process commands
    """

    class MyBot(Bot):
        "Reverse bot, welcoming"

        def default_response(self, in_message):
            return in_message[::-1]

        @command
        def start(self):
            "Welcome the user as first thing!"
            return "Welcome!"

    bot = create_bot(MyBot, HttpEndpoint)

    resp = send_to_http_bot(bot, "/start")

    assert resp.status_code == 200
    ret = json.loads(resp.text)
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

    assert bot1.endpoints[0]._port != bot2.endpoints[0]._port

    resp = send_to_http_bot(bot1, "/start")
    assert resp.status_code == 200

    resp = send_to_http_bot(bot2, "/start")
    assert resp.status_code == 200

    bot1.stop()
    bot2.stop()
