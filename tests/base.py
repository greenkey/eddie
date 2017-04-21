""" Tests for the main class of eddie: eddie.bot.Bot
"""

from eddie.bot import Bot


def test_create_bot_object():
    "Very dumb test"

    bot = Bot()
    assert isinstance(bot, Bot)


def test_default_behaviour():
    """ The bot processes input messages getting output from the
        `default_response` method
    """

    class MyBot(Bot):
        "Echo bot"

        def default_response(self, in_message):
            return in_message

    bot = MyBot()
    assert bot.process("hello") == "hello"
    assert bot.process("123") == "123"
    assert bot.process("/hello") == "/hello"


def test_add_command():
    """ Putting the `@command` decorator on bot methods make them commands, so
        they'll be used when the chat message is meant to be a command (it
        starts with a "/" by default)
    """

    from eddie.bot import command

    class MyBot(Bot):
        "Command bot"

        @command
        def hello(self):
            "hello command, call it with '/hello'"
            return "hello!"

        @command
        def bye(self):
            "bye command, call it with '/bye'"
            return "goodbye..."

    bot = MyBot()
    assert bot.process("/hello") == "hello!"
    assert bot.process("/bye") == "goodbye..."


def test_add_endpoint_start_stop(mocker):
    """ Adding endpoints to the bot, they will be started and stopped whenever
        the bot is
    """

    class MyBot(Bot):
        "Empty bot"
        pass

    endpoint = mocker.Mock()

    bot = MyBot()
    bot.add_endpoint(endpoint)
    bot.run()

    assert endpoint.run.called

    bot.stop()

    assert endpoint.stop.called
